# orders/models.py
from django.db import models
from users.models import User
from restaurants.models import Restaurant, MenuItem


class Order(models.Model):
    # Define allowed status choices
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('packing', 'Packing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(
        max_digits=7, decimal_places=2, default=0.00)

    # Use choices for status field
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.menu_item.name} in Order {self.order.id}"
