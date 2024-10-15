from django.urls import path
from .views import RestaurantCreateView, RestaurantListView, MenuItemCreateView, MenuItemListView, LocationListView, AllRestaurantsListView, UserMenuItemListView

urlpatterns = [
    path('location/', LocationListView.as_view(), name='location-list'),
    path('restaurant/', RestaurantCreateView.as_view(), name='restaurant-create'),
    path('restaurants/', RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurants/all/', AllRestaurantsListView.as_view(),
         name='all-restaurant-list'),
    path('menu-item/', MenuItemCreateView.as_view(), name='menu-item-create'),
    path('menu-items/', MenuItemListView.as_view(), name='menu-item-list'),
    path('menu-items/<int:restaurant_id>/',
         UserMenuItemListView.as_view(), name='user-menu-item-list'),
]
