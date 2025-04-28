from django.contrib import admin
from apps.questions.models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "answer_text", "message_id", "created_at")
    search_fields = ("question_text", "answer_text", "message_id")
    list_filter = ("created_at",)
