# orders/serializers.py

from rest_framework import serializers
from .models import Order, OrderItem
# Optional: for validating menu item details
from restaurants.models import MenuItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    # Nested serializer for order items
    order_items = OrderItemSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'restaurant', 'total_price',
                  'status', 'created_at', 'order_items']
        read_only_fields = ['id', 'created_at']  # Make these fields read-only

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)

        for item_data in order_items_data:
            # Create order items associated with the order
            OrderItem.objects.create(order=order, **item_data)

        return order

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('order_items', None)
        instance.status = validated_data.get('status', instance.status)
        instance.total_price = validated_data.get(
            'total_price', instance.total_price)
        instance.save()

        if order_items_data:
            # Clear existing order items and create new ones if provided
            instance.orderitem_set.all().delete()
            for item_data in order_items_data:
                OrderItem.objects.create(order=instance, **item_data)

        return instance
