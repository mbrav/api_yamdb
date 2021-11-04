from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class YamDBTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
