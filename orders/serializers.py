from rest_framework import serializers
from .models import Order, OrderItem
from restaurants.models import Restaurant, MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price']  # Include relevant fields


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name']  # Include relevant fields


class OrderItemSerializer(serializers.ModelSerializer):
    # Use MenuItemSerializer for output representation
    menu_item = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all()  # Accept menu_item as a primary key for input
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'quantity']

    def to_representation(self, instance):
        # Customize the representation to include menu item details
        representation = super().to_representation(instance)
        representation['menu_item'] = MenuItemSerializer(
            instance.menu_item).data
        return representation


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)  # List of order items
    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all()  # Accept restaurant ID
    )

    class Meta:
        model = Order
        fields = ['id', 'restaurant', 'total_price',
                  'status', 'created_at', 'order_items']

    def create(self, validated_data):
        # Print validated data to inspect it
        print("Validated data:", validated_data)
        # Extract order items data
        order_items_data = validated_data.pop('order_items')

        # Get the user from the request context
        user = self.context['request'].user

        # Pop the restaurant from validated_data and create the order
        restaurant = validated_data.pop('restaurant')
        order = Order.objects.create(
            user=user, restaurant=restaurant, **validated_data)

        # Loop through each order item and create the corresponding OrderItem
        for item_data in order_items_data:
            # Get the menu_item ID from the data
            # Access menu_item id directly from the object
            menu_item_id = item_data['menu_item'].id

            # Create OrderItem with the associated order and menu_item
            OrderItem.objects.create(
                order=order,
                menu_item_id=menu_item_id,  # Use menu_item_id directly
                quantity=item_data['quantity']
            )

        return order

    def to_representation(self, instance):
        # Customize the representation to include restaurant details
        representation = super().to_representation(instance)
        representation['restaurant'] = RestaurantSerializer(
            instance.restaurant).data

        # Include order items in the representation
        representation['order_items'] = OrderItemSerializer(
            instance.order_items.all(), many=True).data
        return representation
