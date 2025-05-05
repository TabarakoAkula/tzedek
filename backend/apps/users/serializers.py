from apps.users.models import User
from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    telegram_id = serializers.CharField(max_length=32, required=True)
    username = serializers.CharField(max_length=256, required=False)
    language = serializers.ChoiceField(
        choices=[
            ("RU", "Russian"),
            ("EN", "English"),
            ("HE", "Hebrew"),
        ],
        required=True,
    )
    created_at = serializers.DateTimeField(read_only=True, required=False)

    def create(self, validated_data):
        try:
            user = User.objects.get(telegram_id=validated_data.get("telegram_id"))
        except User.DoesNotExist:
            user = User(
                telegram_id=validated_data.get("telegram_id"),
                username=validated_data.get("username"),
                language=validated_data.get("language"),
            )
            user.save()
        return user

    @staticmethod
    def update_username(validated_data):
        if not User.objects.filter(
            telegram_id=validated_data.get("telegram_id"),
        ).exists():
            raise serializers.ValidationError(
                "User with this telegram_id does not exists",
            )
        user = User.objects.get(telegram_id=validated_data.get("telegram_id"))
        user.username = validated_data.get("username")
        user.save()
        return user

    @staticmethod
    def change_language(validated_data):
        if not User.objects.filter(
            telegram_id=validated_data.get("telegram_id"),
        ).exists():
            raise serializers.ValidationError(
                "User with this telegram_id does not exists",
            )
        user = User.objects.get(telegram_id=validated_data.get("telegram_id"))
        user.language = validated_data.get("language")
        user.save()
        return user
