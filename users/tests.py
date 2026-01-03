from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthTests(APITestCase):
    def test_register_and_get_token(self):
        # регистрация
        reg_payload = {"username": "user_reg", "email": "user_reg@test.com", "password": "StrongPass123!"}
        reg_response = self.client.post("/api/auth/register/", reg_payload, format="json")
        self.assertEqual(reg_response.status_code, status.HTTP_201_CREATED)

        # получение токена
        token_payload = {"username": "user_reg", "password": "StrongPass123!"}
        token_response = self.client.post("/api/auth/token/", token_payload, format="json")
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", token_response.data)
        self.assertIn("refresh", token_response.data)

    def test_set_telegram_chat_id_requires_auth(self):
        payload = {"telegram_chat_id": 123456789}
        response = self.client.post("/api/users/telegram/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_set_telegram_chat_id_success(self):
        user = User.objects.create_user(username="tg_user", email="tg_user@test.com", password="StrongPass123!")
        self.client.force_authenticate(user=user)

        payload = {"telegram_chat_id": 123456789}
        response = self.client.post("/api/users/telegram/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()
        self.assertEqual(user.telegram_chat_id, 123456789)

    def test_set_telegram_chat_id_must_be_unique(self):
        user1 = User.objects.create_user(username="u1", password="StrongPass123!")
        user2 = User.objects.create_user(username="u2", password="StrongPass123!")

        user1.telegram_chat_id = 111
        user1.save(update_fields=["telegram_chat_id"])

        self.client.force_authenticate(user=user2)
        resp = self.client.post("/api/users/telegram/", {"telegram_chat_id": 111}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
