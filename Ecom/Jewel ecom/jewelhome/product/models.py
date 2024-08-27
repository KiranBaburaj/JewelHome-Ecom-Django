from django.db import models
from django.db.models import CASCADE, PROTECT, SET_NULL
from django.db.models import CASCADE, signals



# Create your models here.

class Products(models.Model):  # Use PascalCase for model names
    name = models.CharField(max_length=200)
    description = models.TextField()
    product_images = models.ManyToManyField('Image', blank=True)  # Renamed the field    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Use appropriate max_digits
    tot_price = models.DecimalField(max_digits=6, decimal_places=2,default=0.0)  # Use appropriate max_digits
    discount = models.DecimalField(max_digits=2, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    size = models.IntegerField()
    Category=models.ForeignKey('Category', on_delete=CASCADE, null=True)
    making_charge = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    product_rating = models.ForeignKey('Rating', on_delete=CASCADE, null=True)
    daily_rate = models.ForeignKey('DailyRate', on_delete=CASCADE, null=True)

    




class Image(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='images')
    images= models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='categories/')  # Add upload path for images
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_related_products()  # Call after saving

    def update_related_products(self):
        products = Products.objects.filter(Category=self)
        for product in products:
                if self.is_active:
                    pass
                else:
                    product.is_active = self.is_active
                    product.save()



class DailyRate(models.Model):
    rate = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update all related products when a new DailyRate is created
        self.update_related_products()

    def update_related_products(self):
        # Get all products related to this DailyRate
        related_products = Products.objects.filter(daily_rate=self)
        for product in related_products:
            # Recalculate tot_price based on the new daily_rate
            product.tot_price = (
                self.rate
                + (self.rate * product.making_charge) / 100
                * product.weight
            )
            product.save()

    

class Rating(models.Model):
    rating = models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])

    created_at = models.DateTimeField(auto_now_add=True)
