from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('dry_fruits', 'Dry Fruits'),
        ('flowers','Flowers')
    ]

    name = models.CharField(max_length=100)
    proimage = models.CharField(max_length=100, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, default='')  # New field for description
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    quantity = models.PositiveIntegerField(default=1)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='vegetables')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_product_per_user')
        ]

    def __str__(self):
        return self.name
