from django.urls import path  # Import the path function to define the URL patterns
from base.views import user_views as views  # Import user-related views

# Define URL routes for user management functionality
urlpatterns = [
    # Login route: Obtains JWT token for a user to authenticate them (POST request)
    path('login/', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),  # Login and retrieve JWT token

    # Register route: Allows new users to register (POST request)
    path('register/', views.registerUser, name='register'),  # Register new user

    # Profile route: Retrieves the profile details of the logged-in user (GET request)
    path('profile/', views.getUserProfile, name="users-profile"),  # Get logged-in user profile

    # Profile update route: Updates user profile (PUT/PATCH request)
    path('profile/update/', views.updateUserProfile, name="user-profile-update"),  # Update user profile

    # Users route: Retrieves a list of all users (GET request)
    path('', views.getUsers, name="users"),  # Get all users

    # User by ID route: Retrieves a specific user's details (GET request by user ID)
    path('<str:pk>/', views.getUserById, name='user'),  # Get user by ID

    # Update user route: Updates a specific user's data (PUT/PATCH request by user ID)
    path('update/<str:pk>/', views.updateUser, name='user-update'),  # Update user by ID

    # Delete user route: Deletes a specific user (DELETE request by user ID)
    path('delete/<str:pk>/', views.deleteUser, name='user-delete'),  # Delete user by ID
]

# Md Golam Sharoar Saymum 0242220005101780
