from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields) -> 'CustomUser':
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, password: str = None, **extra_fields) -> 'CustomUser':
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects: 'CustomUserManager' = CustomUserManager()

    class Meta:
        ordering = ['email']
        indexes = [
            models.Index(fields=['email']),
        ]

    def __str__(self) -> str:
        return f"{self.email}"

    @property
    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None) -> bool:
        # Check if the user has the specified permission
        return self.user_permissions.filter(codename=perm).exists()

    def has_module_perms(self, app_label) -> bool:
        # Check if the user has any permissions for the specified app/module
        return self.user_permissions.filter(content_type__app_label=app_label).exists()
