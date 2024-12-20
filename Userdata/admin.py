from django.contrib import admin
from .models import UserProfile,ShoppingCartItem,ProductOrder

# Register the UserProfile model with the admin site
admin.site.register(UserProfile)
admin.site.register(ShoppingCartItem)
admin.site.register(ProductOrder)
