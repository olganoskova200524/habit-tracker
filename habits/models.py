from django.conf import settings
from django.db import models


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
    )
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)

    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_to",
    )

    periodicity = models.PositiveSmallIntegerField(default=1)
    reward = models.CharField(max_length=255, null=True, blank=True)
    duration_seconds = models.PositiveSmallIntegerField()

    is_public = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    last_reminder_sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.user}: {self.action} at {self.time}"
