from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from apps.account.models import CustomUser, Profile



User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=8, required=True, write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm', 'last_name', 'first_name'
        ]

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')

        if password_confirm != password:
            raise ValueError('Пароли не совпадают')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user



class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordConfirmSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, required=True)
    new_password = serializers.CharField(min_length=8, write_only=True, required=True)
    new_password_confirm = serializers.CharField(min_length=8, write_only=True, required=True)

    def validate(self, attrs):
        p1 = attrs.get('new_password')
        p2 = attrs.pop('new_password_confirm')

        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')


        if not email or not password:
            raise serializers.ValidationError('Укажите email и пароль.')


        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь с таким email не найден.')


        user = authenticate(
            request=self.context.get('request'),
            email=email.lower(),
            password=password
        )

        if not user:
            raise serializers.ValidationError('Неверный email или пароль.')


        attrs['user'] = user
        return attrs

class ResetPasswordConfirmSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, required=True)
    new_password = serializers.CharField(min_length=8, write_only=True, required=True)
    new_password_confirm = serializers.CharField(min_length=8, write_only=True, required=True)

    def validate(self, attrs):
        p1 = attrs.get('new_password')
        p2 = attrs.pop('new_password_confirm')

        if p1 != p2:
            raise serializers.ValidationError('Passwords didn\'t match')
        return attrs

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['user']