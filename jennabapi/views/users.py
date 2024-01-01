from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from jennabapi.models import ShuttleUser




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "password", "first_name", "last_name", "email"]
        extra_kwargs = {"password": {"write_only": True}}
        
class ShuttleUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ShuttleUser
        fields = ("user", "active", "bio","rate")
        
class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
