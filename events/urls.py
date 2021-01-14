from django.urls import path, include
from rest_framework.routers import DefaultRouter
from events import views

router = DefaultRouter()
router.register('tiposEvent', views.TipoEventViewSet)
router.register('eventos', views.EventViewSet)
router.register('filteredEvents', views.FilteredEventViewSet)
router.register('getTypes', views.GetOnlyTipoViewSet)
router.register('userCreateEvent', views.UserEventCreateViewSet)

app_name = 'events'


urlpatterns = [
    path('update/<int:pk>', views.UpdateTypeView.as_view(), name='update'),
    path('', include(router.urls))
]
