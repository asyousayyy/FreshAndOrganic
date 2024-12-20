
from django.contrib import admin
from django.urls import path, include
from Userdata import views as views
from usercart import views as views1
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('main.html', views.home,name="home"),
    path('flowers.html',views.flowers,name='flowers'),
    path('fruits.html',views.fruits,name="fruits"),
    path('vegetable.html',views.vegetables,name="vegetables"),
    path('dryfruits.html',views.dry_fruits,name='dry_fruits'),
    path('contact.html',views1.contact_us,name='contact'),
    path('about.html',views.about,name='about'),
    path('signup.html',views.signup,name='signup'),
    path('login.html',views.user_login,name='login'),
    path('personal.html',views.personal,name='personal'),
    path('logout/',views.logout_user,name="logout"),
    path('changepswd.html',views.change_password,name='changepswd'),
    path('editprofile.html',views.editprofile,name='editprofile'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart.html', views.view_cart, name='view_cart'),
    path('update_quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('userproducts.html', views1.user_products_view, name='userproducts'),
    path('editproduct/<str:product_name>/', views1.product_form, name='editproduct'),
    path('addproduct/', views1.product_form, name='addproduct'),
    path('deleteproduct/<str:product_name>/', views1.delete_product, name='deleteproduct'),
     path('product/<int:product_id>/<slug:product_name>/', views.product_detail, name='product_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('ordered-products/', views.ordered_products, name='ordered_products'),
    path('pay-for-order/<int:order_id>/', views.pay_for_order, name='pay_for_order'),
    path('payment-success/<int:order_id>/', views.payment_success, name='payment_success')




]

