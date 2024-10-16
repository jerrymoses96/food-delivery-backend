from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from restaurants.models import Restaurant


# View for Normal Users to create orders and list their own orders
class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only see their own orders
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={
                                         'request': request})  # Pass request in context
        if serializer.is_valid():
            order = serializer.save()  # The user is set automatically in the serializer
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for Restaurant Owners to list orders related to their restaurant
class RestaurantOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Fetch the restaurant owned by the current user
        restaurant = Restaurant.objects.filter(owner=self.request.user).first()
        if restaurant:
            # Fetch orders for the restaurant
            return Order.objects.filter(restaurant=restaurant)
        return Order.objects.none()


# View for Restaurant Owners to update the status of an order
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        order = self.get_object()

        # Only the owner of the restaurant can update the status
        if request.user != order.restaurant.owner:
            return Response({'error': 'You are not authorized to update this order.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Partial update for order status
        serializer = self.get_serializer(
            order, data=request.data, partial=True)
        if serializer.is_valid():
            order = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View to create and list order items (optional, as part of order creation process)
class OrderItemListCreateView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order_item = serializer.save()  # Create the order item
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View to update, retrieve, and delete specific order items
class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
