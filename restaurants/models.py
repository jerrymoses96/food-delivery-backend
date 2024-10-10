from django.db import models
from users.models import User


class Location(models.Model):
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.city


class Restaurant(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    # ImageField for restaurant image
    image = models.ImageField(
        upload_to='restaurant_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(
        blank=True, null=True)  # New description field
    # ImageField for menu item image
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)

    
    def __str__(self):
        return self.name