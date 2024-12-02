from rest_framework import serializers  # Importing the serializers module to handle model serialization
from django.contrib.auth.models import User  # Importing the built-in User model for user-related data
from rest_framework_simplejwt.tokens import RefreshToken  # For generating JWT tokens
from .models import Product, Order, OrderItem, ShippingAddress, Review  # Importing models for product, order, and reviews


# Serializer for User model, extending the base ModelSerializer to convert User objects into JSON
class UserSerializer(serializers.ModelSerializer):
    # Custom fields to return additional user details
    name = serializers.SerializerMethodField(read_only=True)  # Read-only field to return the user's name
    _id = serializers.SerializerMethodField(read_only=True)  # Read-only field for the user ID
    isAdmin = serializers.SerializerMethodField(read_only=True)  # Read-only field to check if the user is an admin

    class Meta:
        model = User  # Indicates that this serializer works with the User model
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin']  # Fields to be included in the serialized data

    # Custom method to return user ID
    def get__id(self, obj):
        return obj.id

    # Custom method to return the user's admin status
    def get_isAdmin(self, obj):
        return obj.is_staff  # Returns True if the user is an admin (staff member)

    # Custom method to return the user's name, or email if no name is provided
    def get_name(self, obj):
        name = obj.first_name  # Trying to fetch the first name
        if name == '':  # If no first name, fallback to email
            name = obj.email
        return name  # Return either the first name or email


# A subclass of UserSerializer that also includes a JWT token for authentication
class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)  # Read-only field for the authentication token

    class Meta:
        model = User  # Indicating the use of the User model
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin', 'token']  # Including the token field

    # Method to generate and return a JWT token for the user
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)  # Generates a new refresh token for the user
        return str(token.access_token)  # Returns the access token as a string


# Serializer for the Review model
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review  # Specifies the Review model
        fields = '__all__'  # Include all fields in the serialized data


# Serializer for the Product model, includes related reviews through a nested serializer
class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)  # Read-only field to fetch related reviews

    class Meta:
        model = Product  # Indicates that this serializer is for the Product model
        fields = '__all__'  # Include all fields of the Product model in the serialized data

    # Method to get all reviews related to the product
    def get_reviews(self, obj):
        reviews = obj.review_set.all()  # Fetch all related reviews for this product
        serializer = ReviewSerializer(reviews, many=True)  # Serialize the reviews
        return serializer.data  # Return the serialized review data


# Serializer for the ShippingAddress model
class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress  # Specifies the ShippingAddress model
        fields = '__all__'  # Include all fields in the serialized data


# Serializer for the OrderItem model
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem  # Specifies the OrderItem model
        fields = '__all__'  # Include all fields in the serialized data


# Serializer for the Order model, including nested order items, shipping address, and user data
class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)  # Read-only field for order items
    shippingAddress = serializers.SerializerMethodField(read_only=True)  # Read-only field for shipping address
    user = serializers.SerializerMethodField(read_only=True)  # Read-only field for user data

    class Meta:
        model = Order  # Indicates that this serializer works with the Order model
        fields = '__all__'  # Include all fields of the Order model in the serialized data

    # Method to get all items related to the order
    def get_orderItems(self, obj):
        items = obj.orderitem_set.all()  # Fetch all order items for this order
        serializer = OrderItemSerializer(items, many=True)  # Serialize the order items
        return serializer.data  # Return the serialized order item data

    # Method to get the shipping address for the order
    def get_shippingAddress(self, obj):
        try:
            address = ShippingAddressSerializer(obj.shippingaddress, many=False).data  # Serialize the shipping address
        except:
            address = False  # If no address is available, return False
        return address  # Return the serialized shipping address data

    # Method to get user details associated with the order
    def get_user(self, obj):
        user = obj.user  # Fetch the user associated with the order
        serializer = UserSerializer(user, many=False)  # Serialize the user data
        return serializer.data  # Return the serialized user data


# **OOP Concepts Explained:**
# 1. **Encapsulation**: Data is encapsulated within the models, and serializers act as an interface to expose the data in a controlled manner.
# 2. **Inheritance**: The `UserSerializerWithToken` inherits from `UserSerializer`, extending its functionality to include the token field. This allows code reuse and promotes DRY (Don't Repeat Yourself) principles.
# 3. **Abstraction**: By using serializers, complex data manipulations and model representations are abstracted away. The user of the API does not need to know the internals of how the data is stored or fetched.
# 4. **Polymorphism**: Methods like `get_reviews`, `get_orderItems`, and `get_shippingAddress` can be customized in their behavior for different models but share the same function name across different serializer classes.

# Md Golam Sharoar Saymum _
# 0242220005101780
