from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "bio"]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = User.objects.filter(username=username).first()
        if not user:
            raise serializers.ValidationError("User not found")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        # attach user for view usage
        attrs["user"] = user
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "bio", "password", "confirm_password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        validated_data["password"] = make_password(validated_data["password"])
        return User.objects.create(**validated_data)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get("email")
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("If email exists, reset link sent.")
        attrs["user"] = user
        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        if new_password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        return attrs
