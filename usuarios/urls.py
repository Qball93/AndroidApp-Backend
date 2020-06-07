from django.urls import path
from usuarios import views

app_name = 'usuarios'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('token/', views.CreateTokenView.as_view(), name='token')
]