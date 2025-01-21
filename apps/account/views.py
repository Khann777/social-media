from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from knox.models import AuthToken

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from apps.account.tasks import send_activation_email_task, send_reset_password_email_task
from apps.generals.send_mail import send_activation_email, send_reset_password_email

from .serializers import RegisterSerializer, LoginSerializer
from .models import UserResetPasswordToken
from ..generals.generate_reset_token import generate_reset_password_token

User = get_user_model()

class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if user:
            try:
                send_activation_email_task.delay(email=user.email, code=user.activation_code)
            except Exception as e:
                return Response({
                    'msg':'Во время отправки письма возникла ошибка',
                    'data': serializer.data
                }, status=201)
            return Response(serializer.data, status=201)

class ActivateView(APIView):
    def get(self, request):
        activation_code = request.query_params.get('u')
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active=True
        user.activation_code=('')
        user.save()
        return Response({
            'msg': 'Succesffuly activated your account'
        })



class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token = AuthToken.objects.create(user)

        return Response({
            'token': token[1],
        }, status=status.HTTP_200_OK)




