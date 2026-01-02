from rest_framework import serializers

from .models import Habit
from .validators import HabitData, validate_habit


class HabitSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = (
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_pleasant",
            "related_habit",
            "periodicity",
            "reward",
            "duration_seconds",
            "is_public",
            "created_at",
        )
        read_only_fields = ("created_at",)

    def validate(self, attrs):
        # Поддерживаем partial update: берём значения из instance если не пришли в attrs
        instance = getattr(self, "instance", None)

        is_pleasant = attrs.get("is_pleasant", getattr(instance, "is_pleasant", False))
        related_habit = attrs.get("related_habit", getattr(instance, "related_habit", None))
        reward = attrs.get("reward", getattr(instance, "reward", None))
        duration_seconds = attrs.get(
            "duration_seconds",
            getattr(instance, "duration_seconds", 0),
        )
        periodicity = attrs.get("periodicity", getattr(instance, "periodicity", 1))

        validate_habit(
            HabitData(
                is_pleasant=is_pleasant,
                related_habit=related_habit,
                reward=reward,
                duration_seconds=duration_seconds,
                periodicity=periodicity,
            )
        )
        return attrs
