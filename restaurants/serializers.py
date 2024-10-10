from rest_framework import serializers
from .models import Restaurant, MenuItem, Location


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        # Exclude 'owner' from being required in the request data
        fields = ['id', 'name', 'location',
                  'opening_time', 'closing_time', 'image']
        # OR
        # You can use `fields = '__all__'` but mark 'owner' as read-only like this:
        extra_kwargs = {
            'owner': {'read_only': True}
        }


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'  # You can specify fields if needed


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'city']  # Include ID and city
