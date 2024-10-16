from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'restaurant', 'total_price', 'status',
                  'created_at', 'order_items']  # Remove 'user'

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        # Assign the user inside the serializer logic
        # Access user from the request context
        user = self.context['request'].user
        # Create order with the user
        order = Order.objects.create(user=user, **validated_data)
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
