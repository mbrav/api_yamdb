from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
    )
    username = serializers.CharField(
        required=True,
    )

    def validate(self, attrs):
        if attrs['username'] == 'me':
            raise serializers.ValidationError(
                {"username": "Имя пользователя не может быть 'me'"})

        user_by_email = User.objects.filter(
            email=attrs['email']).exists()
        user_by_username = User.objects.filter(
            username=attrs['username']).exists()

        # Проверка на связь почты и юзернейма
        not_valid = user_by_email != user_by_username
        if user_by_email and not_valid:
            raise serializers.ValidationError(
                {"email": f"Адрес '{attrs['email']}' уже занят"})
        if user_by_username and not_valid:
            raise serializers.ValidationError(
                {"username": f"Юзернейм '{attrs['username']}' уже занят"})

        return attrs

    def create(self, validated_data):
        user, created = User.objects.get_or_create(
            username=validated_data['username'],
            email=validated_data['email'],
            defaults={'is_active': False},
        )

        # Делаем юзера неактивным, пока он не подвертит свой токен
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
    """
    User сериализатор для PATCH запросов с отключенной
    проверкой на username и email.
    """

    class Meta:
        model = User
        lookup_field = 'username'
        fields = ('username', 'email', 'role',
                  'first_name', 'last_name', 'bio')
        extra_kwargs = {
            'password': {'required': False},
        }


class UserCreateSerializer(UserSerializer):
    """
    User сериализатор для POST запросов с включенной
    проверкой на username и email.
    """

    username = serializers.CharField(
        required=True,
    )
    email = serializers.EmailField(
        required=True,
    )

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {'username': 'Такой юзернеймом уже существует'})
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': 'Пользователь с данной почтой уже существует'})
        return email
