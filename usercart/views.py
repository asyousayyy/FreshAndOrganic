from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product
from django.core.mail import send_mail
from django.conf import settings

def contact_us(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Send an email (you'll need to configure email settings in your Django settings)
        try:
            send_mail(
                subject,
                f"Message from {name} ({email}):\n\n{message}",
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],  # Add your contact email address here
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        except Exception as e:
            messages.error(request, 'There was an error sending your message. Please try again later.')
            return redirect('contact')

    return render(request, 'contact.html')

# View to list all products for the user
def user_products_view(request):
    query = request.GET.get('q', '')
    if query:
        # Fetch products matching the search query
        products = Product.objects.filter(user=request.user, name__icontains=query)
    else:
        # Fetch all products for the user
        products = Product.objects.filter(user=request.user)
    
    return render(request, 'userproducts.html', {'products': products})



def product_form(request, product_name=None):
    if product_name:
        # Edit existing product
        product = get_object_or_404(Product, name=product_name, user=request.user)
        form_title = 'Edit Product'
        button_text = 'Update Product'
    else:
        # Create new product
        product = Product(user=request.user)
        form_title = 'Add New Product'
        button_text = 'Add Product'

    if request.method == 'POST':
        # Get product details from form input
        name = request.POST.get('name', '').strip()
        proimage = request.POST.get('proimage', '')
        price = request.POST.get('price', '')
        quantity = request.POST.get('quantity', '')
        category = request.POST.get('category', '')
        description = request.POST.get('description', '').strip()  # Get the description

        # Check if a product with the same name exists for this user
        existing_product = Product.objects.filter(user=request.user, name=name).exclude(id=product.id).first()

        if existing_product:
            # If the name already exists, show an error message
            messages.error(request, f"A product with the name '{name}' already exists.")
        else:
            # If it's valid, save or update the product
            product.name = name
            product.proimage = proimage
            product.price = price
            product.quantity = quantity
            product.category = category
            product.description = description  # Update the description field
            product.save()

            if product_name:
                messages.success(request, 'Product updated successfully.')
            else:
                messages.success(request, 'Product added successfully.')

            return redirect('userproducts')  # Redirect to the product list page

    return render(request, 'editproduct.html', {
        'product': product,
        'form_title': form_title,
        'button_text': button_text
    })

def delete_product(request, product_name):
    # Get the product by its name and user
    product = get_object_or_404(Product, name=product_name, user=request.user)

    if request.method == 'POST':
        product.delete()  # Delete the product
        messages.success(request, f'Product "{product_name}" has been deleted.')
        return redirect('userproducts')  # Redirect to the product list

    return redirect('userproducts')
