from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from usuarios.serializers import UserEventSerializer
from .models import Evento, TipoEvent
from django.contrib.auth import get_user_model
User = get_user_model()


class TipoEventSerializer(serializers.ModelSerializer):
    """Serializer for the Event type object"""

    class Meta:
        model = TipoEvent
        fields = ('nombre', 'id', 'color')


class TipoUpdateSerializer(serializers.ModelSerializer):
    """Serializer for the active Event type Field"""

    class Meta:
        model = TipoEvent
        fields = '__all__'


class CreateEventSerializer(serializers.ModelSerializer):
    """Serializer for the creation of user reported events object"""
    Usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    TipoEvento = serializers.PrimaryKeyRelatedField(queryset=TipoEvent.objects.all())


    class Meta:
        model = Evento
        fields = ('coordsy', 'coordsx', 'fechaEvento', 'Usuario', 'TipoEvento', 'id', 'Activo')

class ListEventSerializer(serializers.ModelSerializer):
    """Serializer for the list views of event objects"""
    Usuario = UserEventSerializer(read_only=True)
    TipoEvento = TipoEventSerializer(read_only=True)

    class Meta:
        model = Evento
        fields = ('coordsy', 'coordsx', 'fechaEvento', 'Usuario', 'TipoEvento', 'id', 'Activo')
        Depth = 1
