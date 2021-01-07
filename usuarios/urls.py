from django.urls import path, include
from rest_framework.routers import DefaultRouter
from usuarios import views

router = DefaultRouter()
router.register('myUser', views.UsuarioViewSet)
router.register('simpleUser', views.SimpleUserView)

app_name = 'usuarios'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('all/', views.ListUsers.as_view(), name='all'),
    path('update/<int:pk>/', views.UpdateUserView.as_view(), name='update'),
    path('', include(router.urls))
]