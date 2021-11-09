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
                {"username": "Имя пользователя не может быть 'me'"})
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

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {'username': 'Пользователь с данным юзернеймом уже существует'})
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': 'Пользователь с данной почтой уже существует'})
        return email

    class Meta:
        model = User
        lookup_field = 'username'
        fields = ('username', 'email', 'role',
                  'first_name', 'last_name', 'bio')
        extra_kwargs = {
            'password': {'required': False},
        }
