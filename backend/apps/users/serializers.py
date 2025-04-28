from rest_framework import serializers
from apps.users.models import Users


class UsersSerializer(serializers.Serializer):
    telegram_id = serializers.CharField(max_length=32, required=True)
    username = serializers.CharField(max_length=256, required=False)
    created_at = serializers.DateTimeField(read_only=True, required=False)

    def create(self, validated_data):
        if Users.objects.filter(telegram_id=validated_data.get("telegram_id")).exists():
            raise serializers.ValidationError("User with this telegram_id already exists")
        user = Users(
            telegram_id=validated_data.get("telegram_id"),
            username=validated_data.get("username"),
        )
        user.save()
        return user

    def update_username(self, validated_data):
        if not Users.objects.filter(telegram_id=validated_data.get("telegram_id")).exists():
            raise serializers.ValidationError("User with this telegram_id does not exists")
        user = Users.objects.get(telegram_id=validated_data.get("telegram_id"))
        user.username = validated_data.get("username")
        user.save()
        return user
