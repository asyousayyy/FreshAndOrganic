
from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from .models import UserProfile,ShoppingCartItem,ProductOrder
from usercart.models import Product
import stripe
from django.conf import settings


def ordered_products(request):
    # Fetch orders for the logged-in user
    orders = ProductOrder.objects.filter(user=request.user).order_by('-order_date')

    context = {
        'orders': orders,
    }
    return render(request, 'ordered_products.html', context)



stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def pay_for_order(request, order_id):
    if request.method == "POST":
        # Fetch the specific order
        order = ProductOrder.objects.get(id=order_id, user=request.user)

        if order.is_paid:
            return redirect('order_summary')  # If already paid, redirect to the summary page

        # Handle online payment with Stripe
        total_amount = int(order.product.price * order.quantity)+5  # Amount in cents

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f'Order {order_id} Payment',
                    },
                    'unit_amount': int(total_amount * 100),  # Amount in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(f'/payment-success/{order_id}/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
        )

        return redirect(session.url, code=303)

    return render(request, 'main.html', {'order': ProductOrder.objects.get(id=order_id, user=request.user)})


def payment_success(request, order_id):
    # Fetch the order and update the payment status
    order = ProductOrder.objects.get(id=order_id, user=request.user)
    if not order.is_paid:
        order.is_paid = True
        order.save()

    return render(request, 'success.html')

def checkout(request):
    if request.method == "POST":
        # Handle the COD option
        is_cod = 'cod' in request.POST

        if is_cod:
            # Process COD order
            cart_items = ShoppingCartItem.objects.filter(user=request.user)
            total_amount = sum(item.product.price * item.quantity for item in cart_items) + 1
            # Store a flag in the session to indicate COD
            request.session['payment_status'] = 'cod'
            return redirect('success')  # Redirect to a success page
        else:
            # Handle online payment with Stripe
            cart_items = ShoppingCartItem.objects.filter(user=request.user)
            total_amount = sum(item.product.price * item.quantity for item in cart_items)

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Cart Checkout',
                        },
                        'unit_amount': int(total_amount * 100),  # Amount in cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/cancel/'),
            )
            return redirect(session.url, code=303)

    return render(request, 'main.html')


def success(request):
    # Get the payment status from the session
    payment_status = request.session.get('payment_status', 'online')

    # Get all cart items for the current user
    cart_items = ShoppingCartItem.objects.filter(user=request.user)

    # Iterate through cart items to create ProductOrder and update Product quantity
    for item in cart_items:
        # Create a ProductOrder record
        ProductOrder.objects.create(
            user=request.user,
            product=item.product,
            quantity=item.quantity,
            is_paid=(payment_status == 'online')  # Set to True if online payment was successful
        )

        # Update Product quantity
        product = item.product
        product.quantity -= item.quantity
        product.save()

    # Clear the cart items after successful processing
    cart_items.delete()

    # Clear the payment status from the session
    if 'payment_status' in request.session:
        del request.session['payment_status']

    return render(request, 'success.html')




def cancel(request):
    return render(request, 'cancel.html')



def signup(request):
    if request.method == 'POST':
        # Get the fields from the POST data
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        mobile_number = request.POST.get('mobile_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        try:
            # Create a new user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            profile = UserProfile.objects.get(user=user)
            profile.mobile_number = request.POST['mobile_number']
            profile.address = request.POST['address']
            profile.save()

            messages.success(request, "Account created successfully. You can now log in.")
            return redirect('login')  # Ensure 'login' is the correct URL name for your login view

        except IntegrityError:
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect('signup')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('signup')

    return render(request, 'signup.html')

@login_required
def editprofile(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        # Update the profile fields
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        profile.mobile_number = request.POST['mobile_number']
        profile.address = request.POST['address']

        # Update User model's email field (excluding username since it's not editable)
        user.email = request.POST['email']

        # Save changes to the user and profile models
        user.save()
        profile.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('personal')  # Redirect to the user's personal profile page

    return render(request, 'editprofile.html', {'profile': profile, 'user': user})



@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']

        # Validate the old password
        if not request.user.check_password(old_password):
            messages.error(request, 'Incorrect old password.')
            return redirect('changepswd')

        # Validate the new password
        if new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
            return redirect('changepswd')

        # Change the password
        request.user.set_password(new_password1)
        request.user.save()

        messages.success(request, 'Password changed successfully.')
        return redirect('login')

    return render(request, 'changepswd.html')

@login_required
def personal(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        # Update the User model fields directly
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']

        # Update the UserProfile model fields
        profile.mobile_number = request.POST['mobile_number']
        profile.address = request.POST['address']

        # Save changes to the user and profile models
        user.save()
        profile.save()

        return redirect('personal')  # Redirect to the user's personal profile page

    return render(request, 'personal.html', {'profile': profile, 'user': user})

def home(request):
        return render(request, "main.html")




def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

def vegetables(request):
    query = request.GET.get('q', '')
    if query:
        # Fetch all products where the category is 'vegetables' and name contains the query
        vegetable_products = Product.objects.filter(category='vegetables', name__icontains=query)
    else:
        # Fetch all products where the category is 'vegetables'
        vegetable_products = Product.objects.filter(category='vegetables')

    return render(request, 'vegetable.html', {'products': vegetable_products})

def dry_fruits(request):
    query = request.GET.get('q', '')
    if query:
        # Fetch all products where the category is 'dry fruits' and name contains the query
        dry_fruit_products = Product.objects.filter(category='dry_fruits', name__icontains=query)
    else:
        # Fetch all products where the category is 'dry fruits'
        dry_fruit_products = Product.objects.filter(category='dry_fruits')

    return render(request, 'dryfruits.html', {'products': dry_fruit_products})


def fruits(request):
    query = request.GET.get('q', '')
    if query:
        # Fetch all products where the category is 'fruits' and name contains the query
        fruit_products = Product.objects.filter(category='fruits', name__icontains=query)
    else:
        # Fetch all products where the category is 'fruits'
        fruit_products = Product.objects.filter(category='fruits')

    return render(request, 'fruits.html', {'products': fruit_products})

def flowers(request):
    query = request.GET.get('q', '')
    if query:
        # Fetch all products where the category is 'fruits' and name contains the query
        fruit_products = Product.objects.filter(category='flowers', name__icontains=query)
    else:
        # Fetch all products where the category is 'fruits'
        fruit_products = Product.objects.filter(category='flowers')

    return render(request, 'flowers.html', {'products': fruit_products})







def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the user profile page after successful login
        else:
            # If authentication fails, show an error message on the login page
            messages.error(request, "Incorrect username or password")
            context = {'error': 'Invalid credentials. Please try again.'}
            return render(request, 'login.html', context)

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('home')





def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.error(request, "Log in your account to add products to the cart")
        # Redirect to the login page if the user is not authenticated
        return redirect('login')

    # Get the product by id
    product = get_object_or_404(Product, pk=product_id)

    # Try to get or create the ShoppingCartItem for this user and product
    cart_item, created = ShoppingCartItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        # If the item already exists in the cart, increase the quantity
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')  # Redirect to the cart view after adding the product
def product_detail(request, product_id, product_name):
    # Get the product by id
    product = get_object_or_404(Product, pk=product_id)

    # Ensure the product name matches the given name
    if product_name != product.name.replace(' ', '-').lower():
        return redirect('product_detail', product_id=product.id, product_name=product.name.replace(' ', '-').lower())

    # Render the product detail page with the selected product
    return render(request, 'product_details.html', {'product': product})



def view_cart(request):
    cart_items = ShoppingCartItem.objects.filter(user=request.user)
    subtotal = 0
    for item in cart_items:
        item_price = Decimal(str(item.product.price))
        item_quantity = Decimal(str(item.quantity))
        item_subtotal = item_price * item_quantity
        item.subtotal = item_subtotal  # Add subtotal to each cart item
        subtotal += item.product.price * item.quantity

    shipping = Decimal('5.00')  # Assuming a flat shipping rate of $5.00
    total = subtotal + shipping

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
             }

    return render(request, 'view_cart.html', context)


def update_quantity(request, item_id):
    cart_item = get_object_or_404(ShoppingCartItem, id=item_id, user=request.user)
    product = cart_item.product

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'decrease':
            # Decrease quantity, but not below 1
            cart_item.quantity = max(cart_item.quantity - 1, 1)
        elif action == 'increase':
            # Check if the product is out of stock or if max limit reached
            max_quantity = min(10, product.quantity)

            if cart_item.quantity >= max_quantity:
                # Set an error message and don't increase the quantity
                messages.error(request, "Cannot add more of this product. Stock limit reached.")
            else:
                # Increase quantity, but not beyond the available stock
                cart_item.quantity += 1

        cart_item.save()

    return redirect('view_cart')


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(ShoppingCartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')







