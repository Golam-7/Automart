from django.db import models
from django.contrib.auth.models import User

# Models for the application. These define the structure of the database tables for the application.

class Product(models.Model):
    # The Product model stores information about products in the store.
    # Fields include name, image, brand, category, description, rating, price, stock count, etc.

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Reference to the user who added the product
    name = models.CharField(max_length=200, null=True, blank=True)  # Name of the product
    image = models.ImageField(null=True, blank=True, default='/placeholder.png')  # Product image
    brand = models.CharField(max_length=200, null=True, blank=True)  # Product brand
    category = models.CharField(max_length=200, null=True, blank=True)  # Product category
    description = models.TextField(null=True, blank=True)  # Product description
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)  # Product rating (0-5 scale)
    numReviews = models.IntegerField(null=True, blank=True, default=0)  # Number of reviews for the product
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)  # Product price
    countInStock = models.IntegerField(null=True, blank=True, default=0)  # Available stock
    createdAt = models.DateTimeField(auto_now_add=True)  # Timestamp when the product was added
    _id = models.AutoField(primary_key=True, editable=False)  # Unique ID for each product (primary key)

    def __str__(self):
        return self.name  # Return product name when the object is printed


class Review(models.Model):
    # The Review model stores information about product reviews.
    # Fields include the product being reviewed, rating, comment, and the user who created the review.

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)  # Reference to the product being reviewed
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # User who wrote the review
    name = models.CharField(max_length=200, null=True, blank=True)  # Name of the user who wrote the review
    rating = models.IntegerField(null=True, blank=True, default=0)  # Rating (0-5)
    comment = models.TextField(null=True, blank=True)  # Review comment
    createdAt = models.DateTimeField(auto_now_add=True)  # Timestamp when the review was created
    _id = models.AutoField(primary_key=True, editable=False)  # Unique ID for each review

    def __str__(self):
        return str(self.rating)  # Return rating when the review object is printed


class Order(models.Model):
    # The Order model stores information about customer orders.
    # Fields include user details, payment method, shipping details, and timestamps.

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Reference to the user who placed the order
    paymentMethod = models.CharField(max_length=200, null=True, blank=True)  # Payment method used for the order
    taxPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)  # Tax price
    shippingPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)  # Shipping cost
    totalPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)  # Total price of the order
    isPaid = models.BooleanField(default=False)  # Payment status
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)  # Timestamp of payment
    isDelivered = models.BooleanField(default=False)  # Delivery status
    deliveredAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)  # Timestamp of delivery
    createdAt = models.DateTimeField(auto_now_add=True)  # Timestamp when the order was created
    _id = models.AutoField(primary_key=True, editable=False)  # Unique ID for each order

    def __str__(self):
        return str(self.createdAt)  # Return order creation timestamp when the object is printed


class OrderItem(models.Model):
    # The OrderItem model stores information about individual items within an order.
    # It links a product to an order and keeps track of quantity and price.

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)  # Reference to the product being ordered
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)  # Reference to the order
    name = models.CharField(max_length=200, null=True, blank=True)  # Product name in the order
    qty = models.IntegerField(null=True, blank=True, default=0)  # Quantity of the product in the order
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)  # Price per product in the order
    image = models.CharField(max_length=200, null=True, blank=True)  # Image URL for the product
    _id = models.AutoField(primary_key=True, editable=False)  # Unique ID for each order item

    def __str__(self):
        return str(self.name)  # Return product name when the order item object is printed


class ShippingAddress(models.Model):
    # The ShippingAddress model stores the shipping details for an order.

    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)  # One-to-one relationship with Order
    address = models.CharField(max_length=200, null=True, blank=True)  # Shipping address
    city = models.CharField(max_length=200, null=True, blank=True)  # Shipping city
    postalCode = models.CharField(max_length=200, null=True, blank=True)  # Postal code
    country = models.CharField(max_length=200, null=True, blank=True)  # Shipping country
    shippingPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)  # Shipping cost
    _id = models.AutoField(primary_key=True, editable=False)  # Unique ID for the shipping address

    def __str__(self):
        return str(self.address)  # Return address when the shipping address object is printed

# Md Golam Sharoar Saymum _
# 0242220005101780
