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
        write_only=True
    )

    def validate(self, attrs):
        username = attrs['username']
        conf_code = attrs['confirmation_code']

        user = User.objects.filter(username=username)[0]

        if user is None:
            raise serializers.ValidationError(
                {'username': f'A user with username "{username}" is not found.'})

        return attrs

    # class Meta:
    #     model = User
    #     fields = ['username', 'confirmation_code']
    #     extra_kwargs = {
    #         'username': {'required': True},
    #         'confirmation_code': {'required': True}
    #     }


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
