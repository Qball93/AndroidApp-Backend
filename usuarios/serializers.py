from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _
import json




class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'nombre', 'apellido', 'is_admin', 'telefono', 'id', 'is_active', 'last_login')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""

        if validated_data["is_admin"]:
            validated_data.pop("is_admin")
            return get_user_model().objects.create_superuser(**validated_data)
        validated_data.pop("is_admin")
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """update a user, setting the password correctly and return it"""
        print(validated_data)
        password = validated_data.pop('password', None)
        #position = validated_data.pop('position', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

            return user

        else:
            return user
        

class TestUserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'nombre')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    
        
    
class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for user update return"""
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ("nombre", "apellido", "email", "id", "is_admin", "is_active", "telefono", "events", "last_login", "password")


    def update(self, instance, validated_data):
        """update a user, setting the password correctly and return it"""
        print(validated_data)
        password = validated_data.pop('password', None)
        #position = validated_data.pop('position', None)
        user = super().update(instance, validated_data)
        print(user)

        if password:
            print("inside password")
            user.set_password(password)
            user.save()

        return user


class UserEventSerializer(serializers.ModelSerializer):
    """Serialize for the User in relation to event"""

    class Meta:
        model = get_user_model()
        fields = ('nombre', 'apellido', 'email', 'id')

class SimpleUserSerializer(serializers.ModelSerializer):
    """Serializer for a simple user object"""

    class Meta:
        model = get_user_model()
        fields = ('nombre','apellido','id')

class UserAllSerializer(serializers.ModelSerializer):
    """Serializer for the complete User info"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'nombre', 'apellido', 'is_admin', 'telefono',
                  'id', 'last_login', 'events')

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )



    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password

        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
