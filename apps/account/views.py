from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from knox.models import AuthToken

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from apps.account.tasks import send_activation_email_task, send_reset_password_email_task


from .serializers import RegisterSerializer, LoginSerializer, ResetPasswordSerializer,ResetPasswordConfirmSerializer
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
            'msg': 'Успешно активировали ваш аккаунт'
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


class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'msg': 'Пользователь не найден'
            }, status=404)

        reset_code = generate_reset_password_token()
        UserResetPasswordToken.objects.create(user=user, token=reset_code)
        send_reset_password_email_task.delay(email=email, reset_token=reset_code)
        return Response({
            'msg': 'Вам на почту отправлена письмо с инструкцией по сбросу пароля'
        })


class PasswordResetConfirmView(APIView):
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = request.data.get('code')
        new_password = request.data.get('new_password')

        try:
            reset_code = UserResetPasswordToken.objects.get(token=code)
        except UserResetPasswordToken.DoesNotExist:
            return Response({
                'msg': 'Ваш код недействителен'
            }, status=400)

        if not reset_code.is_valid():
            return Response({
                'msg': 'Срок действия вашего кода истек'
            }, status=400)
        user = reset_code.user
        user.set_password(new_password)
        user.save()
        reset_code.delete()
        return Response({
            'msg':'Ваш пароль изменен!'
        }, status=200)
