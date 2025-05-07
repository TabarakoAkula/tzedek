from apps.questions.models import Question
from apps.users.models import User
from rest_framework import serializers


class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="telegram_id",
        queryset=User.objects.all(),
    )

    class Meta:
        model = Question
        fields = "__all__"
