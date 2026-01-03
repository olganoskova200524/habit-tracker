from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit

User = get_user_model()


class HabitBase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            email="user@test.com",
            password="StrongPass123!",
        )
        self.other_user = User.objects.create_user(
            username="other",
            email="other@test.com",
            password="StrongPass123!",
        )

        self.client.force_authenticate(user=self.user)

        # pleasant habit (для related_habit проверок)
        self.pleasant = Habit.objects.create(
            user=self.user,
            place="home",
            time="08:00",
            action="pleasant",
            is_pleasant=True,
            periodicity=1,
            reward=None,
            duration_seconds=60,
            is_public=False,
        )


class HabitValidatorsTests(HabitBase):
    def test_cannot_set_reward_and_related_habit_together(self):
        payload = {
            "place": "office",
            "time": "10:00:00",
            "action": "stretch",
            "is_pleasant": False,
            "related_habit": self.pleasant.id,
            "periodicity": 1,
            "reward": "cookie",
            "duration_seconds": 60,
            "is_public": False,
        }
        response = self.client.post("/api/habits/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duration_seconds_must_be_lte_120(self):
        payload = {
            "place": "home",
            "time": "11:00:00",
            "action": "read",
            "is_pleasant": False,
            "related_habit": None,
            "periodicity": 1,
            "reward": "tea",
            "duration_seconds": 121,
            "is_public": False,
        }
        response = self.client.post("/api/habits/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_periodicity_must_be_1_to_7(self):
        payload = {
            "place": "home",
            "time": "12:00:00",
            "action": "meditate",
            "is_pleasant": False,
            "related_habit": None,
            "periodicity": 8,
            "reward": None,
            "duration_seconds": 60,
            "is_public": False,
        }
        response = self.client.post("/api/habits/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pleasant_cannot_have_reward(self):
        payload = {
            "place": "home",
            "time": "13:00:00",
            "action": "music",
            "is_pleasant": True,
            "related_habit": None,
            "periodicity": 1,
            "reward": "chocolate",
            "duration_seconds": 60,
            "is_public": False,
        }
        response = self.client.post("/api/habits/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_related_habit_must_be_pleasant(self):
        not_pleasant = Habit.objects.create(
            user=self.user,
            place="gym",
            time="14:00",
            action="push ups",
            is_pleasant=False,
            periodicity=1,
            reward=None,
            duration_seconds=60,
            is_public=False,
        )
        payload = {
            "place": "home",
            "time": "15:00:00",
            "action": "study",
            "is_pleasant": False,
            "related_habit": not_pleasant.id,
            "periodicity": 1,
            "reward": None,
            "duration_seconds": 60,
            "is_public": False,
        }
        response = self.client.post("/api/habits/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class HabitCRUDTests(HabitBase):
    def test_create_habit(self):
        payload = {
            "place": "home",
            "time": "09:00:00",
            "action": "drink water",
            "is_pleasant": False,
            "related_habit": None,
            "periodicity": 1,
            "reward": "coffee",
            "duration_seconds": 60,
            "is_public": False,
        }
        response = self.client.post("/api/habits/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)

    def test_update_and_delete_own_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            place="home",
            time="10:00",
            action="old",
            is_pleasant=False,
            periodicity=1,
            reward=None,
            duration_seconds=60,
            is_public=False,
        )

        patch_payload = {"action": "new action"}
        patch_response = self.client.patch(f"/api/habits/{habit.id}/", patch_payload, format="json")
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.data["action"], "new action")

        delete_response = self.client.delete(f"/api/habits/{habit.id}/")
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)


class HabitPermissionsTests(HabitBase):
    def test_user_cannot_access_foreign_habit_detail(self):
        foreign = Habit.objects.create(
            user=self.other_user,
            place="home",
            time="10:00",
            action="foreign",
            is_pleasant=False,
            periodicity=1,
            reward=None,
            duration_seconds=60,
            is_public=False,
        )

        # По твоей логике (queryset только по user) ожидаем 404
        response = self.client.get(f"/api/habits/{foreign.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.patch(f"/api/habits/{foreign.id}/", {"action": "hack"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.delete(f"/api/habits/{foreign.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class HabitPaginationTests(HabitBase):
    def test_list_has_pagination_page_size_5(self):
        Habit.objects.filter(user=self.user).delete()
        for i in range(6):
            Habit.objects.create(
                user=self.user,
                place="home",
                time="09:00",
                action=f"habit {i}",
                is_pleasant=False,
                periodicity=1,
                reward=None,
                duration_seconds=60,
                is_public=False,
            )

        response = self.client.get("/api/habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)

        self.assertEqual(response.data["count"], 6)
        self.assertEqual(len(response.data["results"]), 5)


class PublicHabitsTests(HabitBase):
    def test_public_list_available_without_auth_and_returns_only_public(self):
        Habit.objects.create(
            user=self.user,
            place="home",
            time="20:00",
            action="public habit",
            is_pleasant=False,
            periodicity=1,
            reward="tea",
            duration_seconds=60,
            is_public=True,
        )
        Habit.objects.create(
            user=self.user,
            place="home",
            time="21:00",
            action="private habit",
            is_pleasant=False,
            periodicity=1,
            reward=None,
            duration_seconds=60,
            is_public=False,
        )

        self.client.force_authenticate(user=None)  # снимаем авторизацию
        response = self.client.get("/api/habits/public/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # должны быть только публичные
        for item in response.data["results"]:
            self.assertTrue(item["is_public"])
