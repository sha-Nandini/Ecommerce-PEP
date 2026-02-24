from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} → {self.name}"
        return self.name
    

class Brand(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    discount = models.FloatField(default=0)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    specifications = models.JSONField(blank=True, null=True)
    features = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def discounted_price(self):
        if self.discount:
            return self.price - (self.price * self.discount / 100)
        return self.price

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')

    def __str__(self):
        return f"{self.product.name} Image"
    
class Review(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    rating=models.IntegerField()
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)