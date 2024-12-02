# Import necessary modules and libraries for creating APIs and handling requests.
from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes  # For defining API views and permissions.
from rest_framework.permissions import IsAuthenticated, IsAdminUser  # Built-in DRF permissions.
from rest_framework.response import Response  # Standard response object for APIs.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # Pagination utilities.

from base.models import Product, Review  # Importing the database models.
from base.serializers import ProductSerializer  # Serializer to convert model instances into JSON format.

from rest_framework import status  # For sending HTTP status codes.

# ============================
# API to Fetch All Products
# ============================

@api_view(['GET'])
def getProducts(request):
    """
    Retrieves all products from the database based on a search keyword.
    Supports pagination to limit the number of products displayed per page.

    Args:
        request: HTTP request object containing optional query parameters (e.g., `keyword` and `page`).

    Returns:
        Response: JSON response with paginated product data.
    """
    # Extract the search keyword from the query parameters. Default to an empty string if not provided.
    query = request.query_params.get('keyword')
    if query == None:
        query = ''

    # Filter products by name based on the keyword, and order them by creation date.
    products = Product.objects.filter(
        name__icontains=query).order_by('-createdAt')

    # Handle pagination by extracting the `page` parameter.
    page = request.query_params.get('page')
    paginator = Paginator(products, 5)  # Limit each page to 5 products.

    try:
        products = paginator.page(page)  # Retrieve products for the specified page.
    except PageNotAnInteger:
        products = paginator.page(1)  # Default to page 1 if page is not an integer.
    except EmptyPage:
        products = paginator.page(paginator.num_pages)  # Show the last page if the page is out of range.

    if page == None:
        page = 1

    # Convert page value to an integer for consistency.
    page = int(page)
    print('Page:', page)  # Debugging output to log the page number.

    # Serialize the paginated products and return the response.
    serializer = ProductSerializer(products, many=True)
    return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})


# ============================
# API to Fetch Top Products
# ============================

@api_view(['GET'])
def getTopProducts(request):
    """
    Retrieves the top 5 products with the highest ratings.

    Args:
        request: HTTP request object.

    Returns:
        Response: JSON response with the top-rated product data.
    """
    products = Product.objects.filter(rating__gte=4).order_by('-rating')[0:5]  # Fetch top-rated products.
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# ============================
# API to Fetch a Single Product
# ============================

@api_view(['GET'])
def getProduct(request, pk):
    """
    Retrieves a specific product based on its ID.

    Args:
        request: HTTP request object.
        pk (int): Primary key (ID) of the product.

    Returns:
        Response: JSON response with the product data.
    """
    product = Product.objects.get(_id=pk)  # Retrieve product by ID.
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


# ============================
# Admin API: Create a Product
# ============================

@api_view(['POST'])
@permission_classes([IsAdminUser])  # Restrict access to admin users.
def createProduct(request):
    """
    Creates a new product with default values. Only admins can access this endpoint.

    Args:
        request: HTTP request object.

    Returns:
        Response: JSON response with the newly created product data.
    """
    user = request.user  # Get the admin user who is creating the product.

    # Create a product with default sample values.
    product = Product.objects.create(
        user=user,
        name='Sample Name',
        price=0,
        brand='Sample Brand',
        countInStock=0,
        category='Sample Category',
        description=''
    )

    # Serialize the created product and return the response.
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


# ============================
# Admin API: Update a Product
# ============================

@api_view(['PUT'])
@permission_classes([IsAdminUser])  # Restrict access to admin users.
def updateProduct(request, pk):
    """
    Updates a product based on its ID. Only admins can access this endpoint.

    Args:
        request: HTTP request object containing updated data.
        pk (int): Primary key (ID) of the product.

    Returns:
        Response: JSON response with the updated product data.
    """
    data = request.data
    product = Product.objects.get(_id=pk)  # Retrieve the product to update.

    # Update product fields with new data.
    product.name = data['name']
    product.price = data['price']
    product.brand = data['brand']
    product.countInStock = data['countInStock']
    product.category = data['category']
    product.description = data['description']

    product.save()  # Save changes to the database.

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


# ============================
# Admin API: Delete a Product
# ============================

@api_view(['DELETE'])
@permission_classes([IsAdminUser])  # Restrict access to admin users.
def deleteProduct(request, pk):
    """
    Deletes a product based on its ID. Only admins can access this endpoint.

    Args:
        request: HTTP request object.
        pk (int): Primary key (ID) of the product.

    Returns:
        Response: Confirmation message of deletion.
    """
    product = Product.objects.get(_id=pk)  # Retrieve the product to delete.
    product.delete()
    return Response('Product Deleted')


# ============================
# API: Upload Product Image
# ============================

@api_view(['POST'])
def uploadImage(request):
    """
    Uploads an image for a specific product.

    Args:
        request: HTTP request object containing image data and product ID.

    Returns:
        Response: Confirmation message of successful upload.
    """
    data = request.data

    product_id = data['product_id']  # Extract product ID from the request data.
    product = Product.objects.get(_id=product_id)

    product.image = request.FILES.get('image')  # Save the uploaded image to the product.
    product.save()

    return Response('Image was uploaded')


# ============================
# API: Create a Product Review
# ============================

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Restrict access to authenticated users.
def createProductReview(request, pk):
    """
    Creates a review for a specific product. Checks for duplicate reviews and valid ratings.

    Args:
        request: HTTP request object containing review data.
        pk (int): Primary key (ID) of the product.

    Returns:
        Response: Success or error message.
    """
    user = request.user  # Get the logged-in user.
    product = Product.objects.get(_id=pk)
    data = request.data

    # Check if the user has already reviewed the product.
    alreadyExists = product.review_set.filter(user=user).exists()
    if alreadyExists:
        content = {'detail': 'Product already reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # Validate rating.
    elif data['rating'] == 0:
        content = {'detail': 'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # Create a new review.
    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment'],
        )

        # Recalculate product ratings based on all reviews.
        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating

        product.rating = total / len(reviews)  # Update product rating.
        product.save()

        return Response('Review Added')
    
    """
    The Paginator in Django is a utility for managing pagination, which refers to dividing large data sets into smaller, more manageable pages for display or processing. This is particularly useful when handling a large number of database records, such as products, user accounts, or posts.
    """

# ============================
# End of File
# ============================
# _Md Golam Sharoar Saymum_0242220005101780
