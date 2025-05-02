from apps.questions.models import Question
from django.contrib import admin
from unfold.admin import ModelAdmin


@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    list_display = (
        "get_question_text",
        "get_answer_text",
        "message_id",
        "chat_session_id",
        "success",
        "created_at",
    )
    search_fields = ("question_text", "answer_text", "message_id", "chat_session_id")
    list_filter = ("created_at", "success")

    def get_answer_text(self, obj):
        return str(obj.answer_text)[:50]

    def get_question_text(self, obj):
        return str(obj.question_text)[:50]

    get_answer_text.short_description = "answer"
    get_question_text.short_description = "question"
