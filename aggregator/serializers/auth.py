from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from aggregator.models import User
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
