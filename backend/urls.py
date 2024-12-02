"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin  # Import the admin module to manage site admin interface.
from django.urls import path, include  # Import path for URL routing and include to refer to other URL configurations.

from django.conf import settings  # Import settings to access project-specific configurations.
from django.conf.urls.static import static  # Import to serve static and media files during development.
from django.views.generic import TemplateView  # Import TemplateView for rendering a template.

urlpatterns = [
    path('admin/', admin.site.urls),  # URL for the Django admin interface.
    path('', TemplateView.as_view(template_name='index.html')),  # Default homepage rendered by TemplateView.
    path('api/products/', include('base.urls.product_urls')),  # Include URLs for product-related API views.
    path('api/users/', include('base.urls.user_urls')),  # Include URLs for user-related API views.
    path('api/orders/', include('base.urls.order_urls')),  # Include URLs for order-related API views.
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files during development.
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Serve static files during development.
