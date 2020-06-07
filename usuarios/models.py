from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from usuarios import managers


class Usuario(AbstractBaseUser, PermissionsMixin):
    """Custom user class"""

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # a admin user; non super-user
    is_admin = models.BooleanField(default=False) # a superuser
    nombre = models.CharField(max_length=200, help_text="nombre del usuario")
    apellido = models.CharField(max_length=200, help_text="Apellido del usuario")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido']
    objects = managers.CustomUserManager()

"""class Administrador(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=True) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    nombre = models.CharField(max_length=200, help_text="nombre del usuario")
    apellido = models.CharField(max_length=200, help_text="Apellido del usuario")
    USERNAME_FIELD = 'email'


    @property
    def is_staff(self):
        "Es un administrador?"
        return self.staff

    @property
    def is_admin(self):
        "Es un super usuario?"
        return self.admin

    @property
    def is_active(self):
        "esta activo el usuario?"
        return self.active
"""



