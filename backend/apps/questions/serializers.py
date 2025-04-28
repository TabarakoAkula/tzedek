from rest_framework import serializers
from apps.questions.models import Question
from apps.users.models import User


class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="telegram_id",
        queryset=User.objects.all()
    )

    class Meta:
        model = Question
        fields = "__all__"
