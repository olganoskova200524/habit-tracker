from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    telegram_chat_id = models.BigIntegerField(
        null=True,
        blank=True,
        unique=True,
        help_text="Telegram chat id for reminders",
    )

    def __str__(self) -> str:
        return self.username
