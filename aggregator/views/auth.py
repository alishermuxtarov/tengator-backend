from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from aggregator.models import Token, User, ConfirmationCode
from aggregator.serializers.auth import LoginValidator, LoginDataSerializer, SignInSerializer, ConfirmationSerializer
from aggregator.utils.helpers import integers_only


class LoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginValidator

    def post(self, request):
        data, user = self.serializer_class.check(request.data)
        token = Token.objects.create(user=user)

        return Response(LoginDataSerializer(instance={'token': token.key, 'user': user}).data)


class SignInView(GenericAPIView):
    """
    ### Creates new user by phone if not exists
    ### Sends SMS with confirmation code
    """
    permission_classes = (AllowAny,)
    serializer_class = SignInSerializer
    throttle_key = 'sign_in'

    def post(self, request):
        data = SignInSerializer.check(request.data)
        User.objects.sign_in(data.get('phone'), data.get('country'))
        return Response({}, 201)


class ConfirmationView(GenericAPIView):
    """
    ### Check confirmation code sent by sms
    ### Return authentication token and customer info
    """
    permission_classes = (AllowAny,)
    serializer_class = ConfirmationSerializer

    def post(self, request):
        data = ConfirmationSerializer.check(request.data)
        user = get_object_or_404(User, username=integers_only(data.get('phone')))
        token = Token.objects.create(user=user)
        ConfirmationCode.objects.filter(code=data.get('code'), user=user).update(is_used=True)
        return Response({'token': token.key})
