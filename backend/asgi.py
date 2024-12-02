"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Setting the Django settings module environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Getting the ASGI application callable
application = get_asgi_application()
