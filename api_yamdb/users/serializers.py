from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def validate(self, attrs):
        if attrs['username'] == 'me':
            raise serializers.ValidationError(
                {"username": "Username cannot be 'me'"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        # Делаем юзера неактивным, пока он не подвердит свой токен
        user.is_active = False
        user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'email']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True}
        }


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True,
    )


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True
    )
    email = serializers.EmailField(
        required=True,
    )

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'required': False}
        }
