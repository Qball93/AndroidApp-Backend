from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from usuarios import managers


class Usuario(AbstractBaseUser, PermissionsMixin):
    """Custom user class"""

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        error_messages={'unique':"Este correo ya esta en uso."}
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # a admin user; non super-user
    is_admin = models.BooleanField(default=False) # a superuser
    nombre = models.CharField(max_length=200, help_text="nombre del usuario")
    apellido = models.CharField(max_length=200, help_text="Apellido del usuario")
    telefono = PhoneNumberField(unique=True, error_messages={'unique':"Este numero de telefono ya esta en uso."})
    events = models.IntegerField(default=0)
    objects = managers.CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    
