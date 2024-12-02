from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from base.models import Product, Order, OrderItem, ShippingAddress
from base.serializers import ProductSerializer, OrderSerializer

from rest_framework import status
from datetime import datetime

# Function to add order items
@api_view(['POST'])  # Restricts this view to HTTP POST requests
@permission_classes([IsAuthenticated])  # Only authenticated users can access this view
def addOrderItems(request):
    """
    Handles the creation of a new order for the authenticated user.

    Steps:
    1. Validates that order items are present in the request data.
    2. Creates an `Order` object linked to the authenticated user.
    3. Creates a `ShippingAddress` for the order.
    4. Creates individual `OrderItem` records and links them to the order.
    5. Updates product stock after order creation.

    OOP Concept Used:
    - **Encapsulation**: The `Order`, `OrderItem`, and `ShippingAddress` models encapsulate order-related data.
    """
    user = request.user  # The currently authenticated user
    data = request.data  # Extract data from the request

    # Validate that the request contains order items
    orderItems = data['orderItems']
    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)

    # (1) Create an order linked to the user
    order = Order.objects.create(
        user=user,
        paymentMethod=data['paymentMethod'],
        taxPrice=data['taxPrice'],
        shippingPrice=data['shippingPrice'],
        totalPrice=data['totalPrice']
    )

    # (2) Create a shipping address for the order
    shipping = ShippingAddress.objects.create(
        order=order,
        address=data['shippingAddress']['address'],
        city=data['shippingAddress']['city'],
        postalCode=data['shippingAddress']['postalCode'],
        country=data['shippingAddress']['country'],
    )

    # (3) Add each item in the order to the database
    for i in orderItems:
        product = Product.objects.get(_id=i['product'])  # Fetch the product by ID

        # Create an order item for the product
        item = OrderItem.objects.create(
            product=product,
            order=order,
            name=product.name,
            qty=i['qty'],
            price=i['price'],
            image=product.image.url,
        )

        # (4) Update stock for the product
        product.countInStock -= item.qty
        product.save()

    # Serialize the created order and return the data
    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)


# Function to get orders for the authenticated user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    """
    Retrieves all orders for the authenticated user.
    """
    user = request.user
    orders = user.order_set.all()  # Access related orders using the reverse relationship
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


# Function to get all orders (Admin only)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrders(request):
    """
    Retrieves all orders. Only accessible to admin users.
    """
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


# Function to get a specific order by ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
    """
    Fetches an order by its ID. Accessible to the order's owner or an admin.

    OOP Concept Used:
    - **Inheritance**: The `Order` model inherits from Django's `models.Model`, 
      extending its behavior to include order-specific fields and methods.
    """
    user = request.user

    try:
        # Retrieve the order by primary key
        order = Order.objects.get(_id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            Response({'detail': 'Not authorized to view this order'},
                     status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)


# Function to mark an order as paid
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk):
    """
    Marks an order as paid and records the payment time.
    """
    order = Order.objects.get(_id=pk)

    order.isPaid = True
    order.paidAt = datetime.now()  # Store the current timestamp
    order.save()

    return Response('Order was paid')


# Function to mark an order as delivered (Admin only)
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateOrderToDelivered(request, pk):
    """
    Marks an order as delivered and records the delivery time.
    """
    order = Order.objects.get(_id=pk)

    order.isDelivered = True
    order.deliveredAt = datetime.now()  # Store the current timestamp
    order.save()

    return Response('Order was delivered')
