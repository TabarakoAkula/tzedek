from django.db import models


LANGUAGES = {
    "RU": "Russian",
    "EN": "English",
    "HE": "Hebrew",
}


class User(models.Model):
    telegram_id = models.CharField(
        max_length=32,
        verbose_name="telegram id",
        unique=True,
    )
    username = models.CharField(
        blank=True,
        null=True,
        verbose_name="username",
        max_length=256,
    )
    language = models.CharField(
        max_length=2,
        choices=LANGUAGES,
        verbose_name="language",
        default="EN",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="creation date",
    )
    access = models.BooleanField(
        default=False,
        verbose_name="access",
    )

    def update_username(self, username: str):
        self.username = username
        self.save()

    def __str__(self):
        return str(self.telegram_id)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
