from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_normal_user = models.BooleanField(default=False)
    is_restaurant_owner = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Specify related names for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Unique related name for groups
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        # Unique related name for user_permissions
        related_name='custom_user_permissions',
        blank=True,
    )
