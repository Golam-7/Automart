from django.urls import path  # Importing the 'path' function to define URL patterns
from base.views import product_views as views  # Importing views related to product management

# URL pattern definitions for handling product-related requests
urlpatterns = [
    # Route to fetch all products (GET request) - mapped to the getProducts view
    path('', views.getProducts, name="products"),  # View all products

    # Route to create a new product (POST request) - mapped to the createProduct view
    path('create/', views.createProduct, name="product-create"),  # Create a new product

    # Route to upload product images (POST request) - mapped to the uploadImage view
    path('upload/', views.uploadImage, name="image-upload"),  # Upload product image

    # Route to create a review for a specific product (POST request) - mapped to the createProductReview view
    path('<str:pk>/reviews/', views.createProductReview, name="create-review"),  # Create product review

    # Route to fetch the top-rated products (GET request) - mapped to the getTopProducts view
    path('top/', views.getTopProducts, name='top-products'),  # View top-rated products

    # Route to fetch details of a specific product by its primary key (GET request) - mapped to the getProduct view
    path('<str:pk>/', views.getProduct, name="product"),  # View a specific product

    # Route to update an existing product (PUT/PATCH request) - mapped to the updateProduct view
    path('update/<str:pk>/', views.updateProduct, name="product-update"),  # Update an existing product

    # Route to delete a specific product (DELETE request) - mapped to the deleteProduct view
    path('delete/<str:pk>/', views.deleteProduct, name="product-delete"),  # Delete a product
]

