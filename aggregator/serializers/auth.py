from datetime import timedelta, datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from aggregator.models import User, ConfirmationCode
from aggregator.utils.helpers import integers_only
from aggregator.utils.serializers import ValidatorSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class LoginValidator(ValidatorSerializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)

    def validate(self, data):
        user = User.objects.filter(username=data.get('username')).first()

        if user:
            if not user.is_active:
                raise ValidationError({'username': _("Пользователь не активен")})

            if not user.check_password(data.get('password')):
                raise AuthenticationFailed({'password': _("Неверный пароль")})

            return data, user
        else:
            raise AuthenticationFailed({'username': _("Пользователь не существует")})


class LoginDataSerializer(serializers.Serializer):
    token = serializers.CharField()
    user = UserSerializer()


class SignInSerializer(ValidatorSerializer):
    phone = serializers.CharField(max_length=20)

    def validate(self, data):
        user = User.objects.filter(username=integers_only(data.get('phone'))).first()
        if user:
            if not user.is_active:
                raise ValidationError({'user': _("Пользователь не активен")})

            confirmation = ConfirmationCode.objects.filter(user=user).last()
            if confirmation and confirmation.created_at + timedelta(minutes=1) >= datetime.now():
                raise ValidationError({'user': _("Повторная отправка SMS возможна через 60 секунд")})

        return data


class ConfirmationSerializer(ValidatorSerializer):
    phone = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=20)

    def validate(self, data):
        if not ConfirmationCode.objects.verify(data.get('phone'), data.get('code')):
            raise ValidationError({'code': _("Неверный код подтверждения")})
        return data
