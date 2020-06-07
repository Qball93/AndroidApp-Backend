import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here
class Evento(models.Model):
    """El evento a ser reportado por la patrulla"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='ID unica para el evento')
    coordsx = models.DecimalField(max_digits=12,decimal_places=8)
    coordsy = models.DecimalField(max_digits=12,decimal_places=8)
    idEvento = models.ForeignKey('TipoEvent',on_delete=models.SET_NULL, null= True)
    idUsuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null= True)
    fechaEvento = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        """String que represental el modelo objeto"""
        return f'Evento de {self.idEvento} registrado el {self.fechaEvento}'

    def get_absolute_url(self):
        """Regresa el url con accesso al registro de evento"""
        return reverse('detalle-evento', args=[str(self.id)])


class TipoEvent(models.Model):
    """Representa los diferentes tipos de eventos que se pueden reportar"""
    nombre = models.CharField(max_length=200, help_text="Ingrese el nombre del evento")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='ID unica para el tipo de evento')

    def __str__(self):
        """String que represental el modelo objeto"""
        return self.nombre
