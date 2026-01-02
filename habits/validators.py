from dataclasses import dataclass
from typing import Optional

from rest_framework.serializers import ValidationError

from .models import Habit


@dataclass(frozen=True)
class HabitData:
    """
    Структура данных для передачи и валидации параметров привычки.
    """
    is_pleasant: bool
    """Признак приятной привычки"""

    related_habit: Optional[Habit]
    """Связанная привычка (может быть указана только для полезной привычки)"""

    reward: Optional[str]
    """Награда за выполнение привычки"""

    duration_seconds: int
    """Длительность выполнения привычки в секундах"""

    periodicity: int
    """Периодичность выполнения привычки в днях"""


def validate_habit(data: HabitData) -> None:
    """
    Выполняет бизнес-валидацию данных привычки согласно ТЗ.
    """

    # Длительность привычки не должна превышать 120 секунд
    if data.duration_seconds > 120:
        raise ValidationError(
            {"duration_seconds": "duration_seconds must be <= 120"}
        )

    # Периодичность должна быть в диапазоне от 1 до 7 дней
    if not (1 <= data.periodicity <= 7):
        raise ValidationError(
            {"periodicity": "periodicity must be between 1 and 7"}
        )

    # Нельзя одновременно указывать награду и связанную привычку
    if data.reward and data.related_habit:
        raise ValidationError(
            "You can't set both reward and related_habit"
        )

    # Связанная привычка может быть только приятной
    if data.related_habit and not data.related_habit.is_pleasant:
        raise ValidationError(
            {"related_habit": "related_habit must be pleasant (is_pleasant=True)"}
        )

    # Приятная привычка не может иметь награду или связанную привычку
    if data.is_pleasant and (data.reward or data.related_habit):
        raise ValidationError(
            "Pleasant habit can't have reward or related_habit"
        )
