from django.db import models
from apps.users.models import User


class Question(models.Model):
    author = models.ForeignKey(
        User,
        related_name="questions",
        on_delete=models.CASCADE,
        verbose_name="author",
    )
    question_text = models.TextField(verbose_name="question")
    answer_text = models.TextField(
        blank=True,
        null=True,
        verbose_name="answer",
    )
    message_id = models.CharField(
        max_length=32,
        verbose_name="message id",
        unique=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="creation date",
    )

    def __str__(self):
        return self.question_text[:20]

    class Meta:
        verbose_name = "question"
        verbose_name_plural = "questions"
