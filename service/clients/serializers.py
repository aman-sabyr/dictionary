from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Client


class LogoutSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['__all__', ]


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    nickname = serializers.CharField(max_length=32, required=True)
    group = serializers.CharField(max_length=10)
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)

    def validated_email(self, email):
        if Client.objects.filter(email=email).exists():
            raise serializers.ValidationError('email is already taken <3')
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('<><><><><><> passwords are not similar <><><><><><>')
        return attrs

    def create(self, validated_data):
        return Client.objects.create_user(**validated_data)


class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)

    def validate_email(self, email):
        if not Client.objects.filter(email=email).exists():
            raise serializers.ValidationError('<><><><><><> user wasn\'t found :( <><><><><><>')
        return email

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        if not Client.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError('<><><><><><> code is incorrect :( <><><><><><>')
        return attrs

    def activate(self, validated_data):
        email = validated_data.get('email')
        client = Client.objects.get(email=email)
        client.is_active = True
        client.activation_code = ''
        client.save()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        if not Client.objects.filter(email=email).exists():
            raise serializers.ValidationError('<><><><><><> user wasn\'t found <><><><><><>')
        return email

    def validate(self, attrs):
        request = self.context.get('request')
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            client = authenticate(username=email, password=password, request=request)
            if not client:
                raise serializers.ValidationError('<><><><><><> password is not correct <><><><><><>')
        else:
            raise serializers.ValidationError('<><><><><><> type ur email or password <><><><><><>')
        attrs.update({'user': client})
        return attrs