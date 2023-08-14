from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.




class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username=None, password=None, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, password, **other_fields)

    def create_user(self, email, username=None, password=None, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        if username == None:
            username = email

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)

        if password is not None:
            user.set_password(password)

        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    STATUS_CHOICES = (
        ('active', 'active'),
        ('inactive', 'inactive'),
        ('banned', 'banned'),
    )

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True,null=True)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    
    is_verified = models.BooleanField(default=False)
    
    email_verified_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True,choices=STATUS_CHOICES)  # active, inactive, banned

    is_staff = models.BooleanField(default=False)
    
    # timestamps
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username





