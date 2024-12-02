from django.db.models.signals import pre_save  # Importing the pre_save signal to perform actions before saving a model
from django.contrib.auth.models import User  # Importing the built-in User model from Django's authentication system


# The updateUser function will be called before saving the User model instance
def updateUser(sender, instance, **kwargs):
    user = instance  # Getting the instance of the user model
    # Check if the user has a non-empty email
    if user.email != '':
        user.username = user.email  # If email is present, set the username to the email address


# Connecting the updateUser function to the pre_save signal of the User model
# This means the updateUser function will be executed before saving a User instance
pre_save.connect(updateUser, sender=User)

# **OOP Concepts Explained:**
# 1. **Encapsulation**: The logic to update the username is encapsulated inside the `updateUser` function, which operates as an interface for modifying the User model instance before it is saved. This keeps the logic within a dedicated method, preventing it from being scattered across other parts of the application.
# 2. **Abstraction**: The `pre_save` signal abstracts away the need for manually checking and updating the username whenever a User model instance is created or modified. The update happens automatically behind the scenes.
# 3. **Inheritance**: The User model inherently inherits the features of the Django model class. The signal function operates in the context of this model, and the mechanism is based on a signal-handler architecture.

# **Author Information:**
# Developed by: Md Golam Sharoar Saymum
# User ID: 0242220005101780
# Additional Information: The `pre_save` signal allows you to hook into the saving process of a model. This ensures that the username is always set to the email before saving, which is often useful for systems where emails serve as unique identifiers.

