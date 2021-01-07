from rest_framework import generics, authentication, permissions, status, viewsets, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from .serializers import UserSerializer, AuthTokenSerializer, UserAllSerializer, UserUpdateSerializer, SimpleUserSerializer, TestUserSerializer
User = get_user_model()

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]


class UsuarioViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
    """Manage Active Users in database"""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['email']

    def get_queryset(self):
        """Return all existing users for the current admin"""
        self.serializer_class = UserSerializer
        #queryset = super(EventViewSet, self).get_queryset()
        queryset = super(UsuarioViewSet, self).get_queryset()
        return queryset

    def perform_create(self, serializer):
        """Create a new event"""
        serializer.save()


class UsuarioNonAdminViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
    """Manage Active Users in database"""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]



class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, create = Token.objects.get_or_create(user=user)
            update_last_login(None, user)  
            return Response({
                'token': token.key,
                'admin': user.is_admin,
                'email': user.email
            })
        else:
            return Response(
                {"msg":"Usuario o password incorrecta"},
                status=status.HTTP_401_UNAUTHORIZED
            )

    #renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UpdateUserView(generics.UpdateAPIView):
    """Update user info"""
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]





class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user



class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        #queryset = User.objects.all()
        #return Response(queryset)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class SimpleUserView(viewsets.ReadOnlyModelViewSet):
    """
        REST API endpoint for 'accommodation' resource
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    queryset = User.objects.all()
    serializer_class = SimpleUserSerializer

    def get_queryset(self):
        qs = User.objects.all()


        return qs