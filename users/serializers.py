from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    def validate_password(self, value: str) -> str:
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class TelegramChatIdSerializer(serializers.Serializer):
    telegram_chat_id = serializers.IntegerField()

    def validate_telegram_chat_id(self, value: int) -> int:
        if value <= 0:
            raise serializers.ValidationError("telegram_chat_id must be positive")
        return value
