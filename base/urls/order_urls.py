from django.urls import path  # Importing path to define URL patterns
from base.views import order_views as views  # Importing the views for order-related endpoints

# URL pattern definitions for handling orders
urlpatterns = [
    # Route to fetch all orders (GET request) - mapped to the getOrders view
    path('', views.getOrders, name='orders'),  # View all orders

    # Route to add order items to an existing order (POST request) - mapped to the addOrderItems view
    path('add/', views.addOrderItems, name='orders-add'),  # Add items to order

    # Route to fetch orders of the currently logged-in user (GET request) - mapped to the getMyOrders view
    path('myorders/', views.getMyOrders, name='myorders'),  # View user's orders

    # Route to update order status to 'Delivered' (PATCH request) - mapped to the updateOrderToDelivered view
    path('<str:pk>/deliver/', views.updateOrderToDelivered, name='order-delivered'),  # Mark order as delivered

    # Route to fetch a specific order by its primary key (GET request) - mapped to the getOrderById view
    path('<str:pk>/', views.getOrderById, name='user-order'),  # View details of a specific order

    # Route to update the order status to 'Paid' (PATCH request) - mapped to the updateOrderToPaid view
    path('<str:pk>/pay/', views.updateOrderToPaid, name='pay'),  # Mark order as paid
]

