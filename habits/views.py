from rest_framework import generics, permissions

from .models import Habit
from .permissions import IsOwner
from .serializers import HabitSerializer


class HabitListCreateView(generics.ListCreateAPIView):
    """
    Список привычек текущего пользователя (пагинация по умолчанию из settings, PAGE_SIZE=5)
    + создание привычки
    """
    serializer_class = HabitSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user).select_related("related_habit")


class HabitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user).select_related("related_habit")


class PublicHabitListView(generics.ListAPIView):
    """
    Список публичных привычек (доступен всем, только чтение).
    """
    serializer_class = HabitSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Habit.objects.filter(is_public=True).select_related("related_habit")
