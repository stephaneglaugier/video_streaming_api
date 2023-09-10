from datetime import date

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import (EmailValidator, MinLengthValidator,
                                    RegexValidator)
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **kwargs):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **kwargs)


class CustomUser(AbstractBaseUser):
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[
            RegexValidator(r'^[a-zA-Z0-9]*$',
                           'Only alphanumeric characters are allowed.')
        ]
    )
    password = models.CharField(
        max_length=128,
        validators=[
            MinLengthValidator(8),
            RegexValidator(
                r'^(?=.*[A-Z])(?=.*\d)', 'Password must contain at least one uppercase letter and one number.')
        ]
    )
    email = models.EmailField(
        validators=[EmailValidator()]
    )
    dob = models.DateField(
        verbose_name="Date of Birth",
        default=date.today
    )
    credit_card_number = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                r'^\d{16}$', 'Credit card number must have 16 digits.')
        ]
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password', 'dob']

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
