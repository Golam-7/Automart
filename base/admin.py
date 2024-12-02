from django.contrib import admin
from .models import *

# Register your models here.

# Register the Product model with the admin site to make it available in the Django admin interface
admin.site.register(Product)

# Register the Review model to allow review management through the admin interface
admin.site.register(Review)

# Register the Order model so that orders can be managed via the Django admin
admin.site.register(Order)

# Register the OrderItem model, which represents individual items in an order
admin.site.register(OrderItem)

# Register the ShippingAddress model to manage shipping details related to orders
admin.site.register(ShippingAddress)

# OOP Concept:
# - **Encapsulation**: The models (`Product`, `Review`, `Order`, etc.) encapsulate the data 
#   and business logic associated with each entity (product, review, order, etc.).
#   By registering these models with the admin site, you're enabling encapsulation 
#   of the model objects for easier management via the Django admin interface.
