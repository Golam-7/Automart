"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os  # Import the os module to interact with operating system functionality (such as setting environment variables).

from django.core.wsgi import get_wsgi_application  # Importing Django’s built-in function to get the WSGI application.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')  
# Encapsulation: Setting the Django settings module environment variable. The internal logic of how Django locates settings is hidden from the user.

application = get_wsgi_application()  # Abstraction: Returning the WSGI application object, which abstracts away details of how requests are handled.
