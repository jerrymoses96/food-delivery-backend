from django.urls import path
from .views import (
    OrderListCreateView,
    OrderDetailView,
    RestaurantOrderListView,
    OrderItemListCreateView,
    OrderItemDetailView,
)

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(),
         name='order-list-create'),  # Create and list users' orders
    path('orders/<int:pk>/', OrderDetailView.as_view(),
         name='order-detail'),  # Retrieve, update, and delete order
    path('restaurant-orders/', RestaurantOrderListView.as_view(),
         name='restaurant-order-list'),  # List restaurant orders
    path('order-items/', OrderItemListCreateView.as_view(),
         name='order-item-list-create'),  # Create and list order items
    path('order-items/<int:pk>/', OrderItemDetailView.as_view(),
         name='order-item-detail'),  # Retrieve, update, and delete order item
]
