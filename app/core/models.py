"""
Database models.
"""
# PYTHON IMPORTS
from sys import _getframe
# DJANGO IMPORTS
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """User Manager overridden from BaseUserManager for User"""

    def _create_user(self, email, password=None, **extra_fields):
        """Creates and returns a new user using an email address"""
        if not email:  # check for an empty email
            raise AttributeError("User must set an email address")
        email = self.normalize_email(email)  # normalize email

        # create user
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # hashes/encrypts password
        user.save(using=self._db)  # save user
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Creates and returns a new user using an email address"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_staffuser(self, email, password=None, **extra_fields):
        """Creates and returns a new staffuser using an email address"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and returns a new superuser using an email address"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """User model that supports using email instead of username"""
    email = models.EmailField(
        _('Email Address'), max_length=255, unique=True
    )
    name = models.CharField(_('Name'), max_length=255)
    is_active = models.BooleanField(
        _('Active'), default=True, null=True
    )
    is_staff = models.BooleanField(
        _('Staff status'), default=False, null=True
    )
    is_superuser = models.BooleanField(
        _('Su status'), default=False, null=True
    )

    objects = UserManager()  # uses the custom manager

    USERNAME_FIELD = 'email'  # overrides username to email field

    def __str__(self):
        """User model string representation"""
        return self.email


class Recipe(models.Model):
    """Recipe object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title
