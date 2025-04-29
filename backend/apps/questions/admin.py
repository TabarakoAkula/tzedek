from apps.questions.models import Question
from django.contrib import admin
from unfold.admin import ModelAdmin


@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    list_display = ("question_text", "answer_text", "message_id", "created_at")
    search_fields = ("question_text", "answer_text", "message_id")
    list_filter = ("created_at",)
