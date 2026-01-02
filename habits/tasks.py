from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_habits_reminders() -> int:
    now = timezone.localtime()
    current_hm = (now.hour, now.minute)

    habits = Habit.objects.filter(user__telegram_chat_id__isnull=False)

    sent = 0
    for habit in habits:
        if (habit.time.hour, habit.time.minute) == current_hm:
            text = f"Reminder: {habit.action} at {habit.place}"
            send_telegram_message(int(habit.user.telegram_chat_id), text)
            sent += 1

    return sent
