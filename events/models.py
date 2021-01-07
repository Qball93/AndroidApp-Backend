import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User






# Create your models here
class TipoEvent(models.Model):
    """Representa los diferentes tipos de eventos que se pueden reportar"""
    nombre = models.CharField(max_length=200, help_text="Ingrese el nombre del evento", null=False)
    Activo = models.BooleanField(default=True)
    color = models.CharField(max_length=12, help_text="Color para el evento")

    def __str__(self):
        """String que represental el modelo objeto"""
        return self.nombre



class Evento(models.Model):
    """El evento a ser reportado por la patrulla"""
    coordsx = models.DecimalField(max_digits=12, decimal_places=8, null=False)
    coordsy = models.DecimalField(max_digits=12, decimal_places=8, null=False)
    TipoEvento = models.ForeignKey(TipoEvent, on_delete=models.CASCADE, null=False)
    Activo = models.BooleanField(default=True, null=False)
    Usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    fechaEvento = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        """String que represental el modelo objeto"""
        return f'Evento de tipo {self.TipoEvento} registrado el {self.fechaEvento}'

    def get_absolute_url(self):
        """Regresa el url con accesso al registro de evento"""
        return reverse('detalle-evento', args=[str(self.id)])
