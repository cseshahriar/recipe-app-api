"""
Database models.
"""
# PYTHON IMPORTS
from sys import _getframe
# DJANGO IMPORTS
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
        else:  # normalizes the provided email
            email = self.normalize_email(email)

        # create user
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # hashes/encrypts password
        user.save(using=self._db)  # safe for multiple databases
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
    # Add related_name to avoid clashes with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='core_user_groups',
        blank=True,
        help_text=_('The groups this user belongs to.'),
        verbose_name=_('groups'),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='core_user_permissions',
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('user permissions'),
    )
    objects = UserManager()  # uses the custom manager

    USERNAME_FIELD = 'email'  # overrides username to email field

    def get_full_name(self):
        """Returns full name of User
        Return None if no names are set"""
        full_name = None  # default

        # join first name and last name
        if self.first_name:
            full_name = ''.join(self.first_name)
            if self.last_name:
                full_name += f' {self.last_name}'
        else:
            if self.last_name:
                full_name = ''.join(self.last_name)

        return full_name  # returns None if no name is set

    def get_phone_intl_format(self, prefix='+88'):
        """Returns phone number in international format
        Default prefix: +88 (Bangladesh code)
        Returns None if user has no phone number saved"""
        phone_intl = f'{prefix}{self.phone}' if self.phone else None
        return phone_intl

    def __str__(self):
        """User model string representation"""
        return self.email
