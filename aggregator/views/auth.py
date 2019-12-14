from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from aggregator.models import Token
from aggregator.serializers.auth import LoginValidator, LoginDataSerializer


class LoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginValidator

    def post(self, request):
        data, user = self.serializer_class.check(request.data)
        token = Token.objects.create(user=user)

        return Response(LoginDataSerializer(instance={'token': token.key, 'user': user}).data)
