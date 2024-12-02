# This module defines API endpoints related to user management, including login, registration,
# profile updates, and administrative user management. It leverages Django REST Framework (DRF) 
# for creating secure and interactive APIs. 
# OOP concepts like inheritance and encapsulation are implemented through the TokenObtainPairView 
# and its custom serializer.

from django.shortcuts import render  # Used for rendering templates, though not utilized here.
from rest_framework.decorators import api_view, permission_classes  # Decorators for API views and permission settings.
from rest_framework.permissions import IsAuthenticated, IsAdminUser  # Built-in DRF permissions.
from rest_framework.response import Response  # Standard DRF response class.

from django.contrib.auth.models import User  # Built-in user model in Django for authentication.
from base.serializers import ProductSerializer, UserSerializer, UserSerializerWithToken  # Custom serializers for the API.
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  # Default serializer for JWT.
from rest_framework_simplejwt.views import TokenObtainPairView  # Default view for obtaining JWT tokens.

from django.contrib.auth.hashers import make_password  # Utility to securely hash passwords.
from rest_framework import status  # HTTP response status codes.

# ============================
# Custom JWT Token Serializer
# ============================

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer to add additional user data into the JWT response.
    Inherits from the TokenObtainPairSerializer to reuse base token logic.
    Demonstrates **Inheritance**: Extending base serializer functionality.
    """
    def validate(self, attrs):
        """
        Overrides the default validate method to include additional user data in the JWT token.
        """
        # Call the parent class's validate method to get the base token data.
        data = super().validate(attrs)

        # Use custom serializer to get additional user data and merge it with the token data.
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token view to use the modified serializer.
    Demonstrates **Encapsulation**: Hiding implementation details by using the custom serializer.
    """
    serializer_class = MyTokenObtainPairSerializer

# ============================
# User Registration API
# ============================

@api_view(['POST'])
def registerUser(request):
    """
    Registers a new user with the provided data (name, email, and password).
    Returns a token for the newly created user.

    Args:
        request: Contains the user's registration data.

    Returns:
        Response: Serialized user data or error message if registration fails.
    """
    data = request.data
    try:
        # Create a new user object with the provided data.
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],  # Username is set to the email for simplicity.
            email=data['email'],
            password=make_password(data['password'])  # Securely hash the password.
        )
        # Serialize the created user with the token.
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        # Handle cases where the email is already registered.
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

# ============================
# Update User Profile API
# ============================

@api_view(['PUT'])
@permission_classes([IsAuthenticated])  # Ensures only authenticated users can access this endpoint.
def updateUserProfile(request):
    """
    Updates the profile of the logged-in user based on the provided data.
    Allows changing name, email, and password.

    Args:
        request: Contains the new profile data.

    Returns:
        Response: Serialized updated user data.
    """
    user = request.user  # Get the logged-in user.
    serializer = UserSerializerWithToken(user, many=False)

    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']

    # Update password only if provided.
    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()  # Save changes to the database.

    return Response(serializer.data)

# ============================
# Retrieve User Profile API
# ============================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    """
    Retrieves the profile data of the logged-in user.

    Args:
        request: Contains the user's authentication token.

    Returns:
        Response: Serialized user data.
    """
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

# ============================
# Admin User Management APIs
# ============================

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    """
    Retrieves a list of all users. Accessible only to admin users.

    Args:
        request: HTTP request object.

    Returns:
        Response: List of serialized user data.
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    """
    Retrieves details of a specific user by their ID. Accessible only to admin users.

    Args:
        request: HTTP request object.
        pk (int): ID of the user to retrieve.

    Returns:
        Response: Serialized user data.
    """
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request, pk):
    """
    Updates a specific user's data. Accessible only to authenticated users.

    Args:
        request: HTTP request object containing updated data.
        pk (int): ID of the user to update.

    Returns:
        Response: Serialized updated user data.
    """
    user = User.objects.get(id=pk)

    data = request.data

    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    user.is_staff = data['isAdmin']

    user.save()  # Save changes to the database.

    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    """
    Deletes a specific user by their ID. Accessible only to admin users.

    Args:
        request: HTTP request object.
        pk (int): ID of the user to delete.

    Returns:
        Response: Confirmation message of deletion.
    """
    userForDeletion = User.objects.get(id=pk)
    userForDeletion.delete()
    return Response('User was deleted')

# ============================
# End of File
# ============================
# _Md Golam Sharoar Saymum_0242220005101780
