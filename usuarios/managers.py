from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Custom class to manage custom user"""

    def create_user(self, email, password, nombre, apellido, telefono):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Usuarios necesitan un correo electornico.')


        user = self.model(
            email=self.normalize_email(email),
            nombre=nombre,
            apellido=apellido,
            telefono=telefono
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password, nombre, apellido, telefono):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono
        )

        user.set_password(password)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, nombre, apellido, telefono):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user
