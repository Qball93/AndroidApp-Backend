from rest_framework import generics, authentication, permissions, status, viewsets, mixins, filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django_filters import Filter, FilterSet
from .serializers import ListEventSerializer, CreateEventSerializer, TipoEventSerializer, TipoUpdateSerializer
from .models import Evento, TipoEvent
from django.utils import timezone
from datetime import datetime, date




class TipoEventViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                       mixins.CreateModelMixin, mixins.UpdateModelMixin):
    """Manage EventType in database"""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    serializer_class = TipoEventSerializer
    queryset = TipoEvent.objects.all()
    filterset_fields = ['Activo']


    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        queryset = super(TipoEventViewSet, self).get_queryset()
        return queryset

    def perform_create(self, serializer):
        """Create a new event Type"""
        serializer.save()



class UpdateTypeView(generics.UpdateAPIView):
    """Update user info"""
    queryset = TipoEvent.objects.all()
    serializer_class = TipoUpdateSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]


    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)



class GetOnlyTipoViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """user view to see type events"""
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = TipoEventSerializer
    queryset = TipoEvent.objects.all()
    filterset_fields = ['Activo']


class EventViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                   mixins.CreateModelMixin, mixins.UpdateModelMixin):
    """Manage Active Events in database"""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = Evento.objects.all()
    serializer_class = CreateEventSerializer
    filterset_fields = ['Usuario__id', 'TipoEvento__id', 'Usuario__email', 'fechaEvento', 'Activo']

    def get_queryset(self):
        """Return all existing events for the current admin"""
        self.serializer_class = ListEventSerializer
        queryset = super(EventViewSet, self).get_queryset()
        return queryset

    def perform_create(self, serializer):
        """Create a new event"""
        serializer.save()

    def perform_update(self, serializer):
        """update event info"""
        serializer.save()



class eventDeleteView(generics.UpdateAPIView, mixins.DestroyModelMixin):
    queryset = Evento.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class UserEventCreateViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """Regular event creation view"""
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = CreateEventSerializer
    queryset = Evento.objects.all()



    def perform_create(self, serializer):
        """adasdadasd"""
        serializer.save(Usuario=self.request.user)


class FilteredEventViewSet(viewsets.ReadOnlyModelViewSet):
    """
        REST API endpoint for 'accommodation' resource
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    queryset = Evento.objects.all()
    serializer_class = ListEventSerializer

    def get_queryset(self):
        id_string = self.request.GET.get('TipoEvento')
        start_date = self.request.GET.get('startDate')
        end_date = self.request.GET.get('endDate')
        id_user = self.request.GET.get('User')
        qs = Evento.objects.all()

        if id_string is not None:
            ids = [int(id) for id in id_string.split(',')]
            qs = qs.filter(TipoEvento_id__in=ids)

        if(end_date):
            end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
            end_date = timezone.make_aware(end_date, None)
            qs = qs.filter(fechaEvento__lte=end_date)

        if(start_date):
            start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
            start_date = timezone.make_aware(start_date, None)
            qs = qs.filter(fechaEvento__gte=start_date)

        if(id_user):
            qs = qs.filter(Usuario_id=id_user)


        return qs
