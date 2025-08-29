from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "password", "password_confirm")

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"]
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        error_messages={
            'blank': 'Имя пользователя обязательно для заполнения',
        }
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        error_messages={
            'blank': 'Пароль обязателен для заполнения'
        }
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                msg = _('Неверное имя пользователя или пароль')
                raise serializers.ValidationError(msg, code='authorization')

            if not user.is_active:
                msg = _('Аккаунт пользователя деактивирован')
                raise serializers.ValidationError(msg, code='authorization')

            attrs['user'] = user
        else:
            msg = _('Необходимо указать имя пользователя и пароль')
            raise serializers.ValidationError(msg, code='authorization')

        return attrs
