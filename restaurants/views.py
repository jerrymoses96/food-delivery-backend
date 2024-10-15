from rest_framework import generics, permissions
from .models import Restaurant, MenuItem, Location
from .serializers import RestaurantSerializer, MenuItemSerializer, LocationSerializer
from django.shortcuts import get_object_or_404

# Restaurant Create and List View


class RestaurantCreateView(generics.CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RestaurantListView(generics.ListAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Restaurant.objects.filter(owner=self.request.user)


# New View for Normal Users to List All Restaurants
class AllRestaurantsListView(generics.ListAPIView):
    queryset = Restaurant.objects.all()  # Return all restaurants
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.AllowAny]  # Allow any user to access


# Menu Item Create and List View

class MenuItemCreateView(generics.CreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        restaurant_id = self.request.data.get('restaurant')
        restaurant = get_object_or_404(
            Restaurant, id=restaurant_id, owner=self.request.user)
        serializer.save(restaurant=restaurant)


class MenuItemListView(generics.ListAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        restaurant_id = self.request.GET.get('restaurant')
        if restaurant_id:
            return MenuItem.objects.filter(restaurant__id=restaurant_id)
        return MenuItem.objects.all()


# New view for normal users to fetch menu items based on restaurant ID
class UserMenuItemListView(generics.ListAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.AllowAny]  # Allow normal users to access

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        if restaurant_id:
            return MenuItem.objects.filter(restaurant__id=restaurant_id)
        return MenuItem.objects.none()  # Return empty queryset if no restaurant_id


# Location List View


class LocationListView(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
