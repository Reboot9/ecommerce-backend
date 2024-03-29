"""
Defines the custom user model and related manager for authentication and authorization purposes.
"""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom manager for the CustomUser model.

    This manager provides methods for creating regular users and superusers with appropriate
    default values. The manager ensures proper normalization of email addresses
    and the secure handling of passwords.
    """

    def create_user(self, email: str, password: str = None, **extra_fields) -> "CustomUser":
        """
        Create and return a regular user with the given email and password.

        :param email: The email address for the user.
        :param password: The user's password.
        :param extra_fields: Additional fields to set on the user model.
        :return: The created CustomUser instance.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, password: str = None, **extra_fields) -> "CustomUser":
        """
        Create and return a superuser with the given email and password.

        :param email: The email address for the superuser.
        :param password: The superuser's password.
        :param extra_fields: Additional fields to set on the superuser model.
        :return: The created CustomUser instance with superuser privileges.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with email as the unique identifier.

    This model extends the AbstractBaseUser and PermissionsMixin provided by Django,
    providing a customizable user model for authentication and permission management.
    """

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: "CustomUserManager" = CustomUserManager()

    class Meta:
        ordering = ["email"]
        indexes = [
            models.Index(fields=["email"]),
        ]

    def __str__(self) -> str:
        """
        Return a string representation of the user.

        :return: The user's email address.
        """
        return f"{self.email}"

    @property
    def get_full_name(self) -> str:
        """
        Return the full name of the user.

        :return: The full name, formatted as "first_name last_name".
        """
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None) -> bool:
        """
        Check if the user has the specified permission.

        :param perm: The permission string.
        :param obj: The object for which the permission is checked (default: None).
        :return: True if the user has the specified permission, False otherwise.
        """
        return self.is_superuser

    def has_module_perms(self, app_label) -> bool:
        """
        Check if the user has any permissions for the specified app/module.

        :param app_label: The label of the app/module.
        :return: True if the user has any permissions for the specified app/module,
        False otherwise.
        """
        return self.is_superuser
