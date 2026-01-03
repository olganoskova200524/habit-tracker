from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, TelegramChatIdSerializer


class RegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class SetTelegramChatIdView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TelegramChatIdSerializer

    @extend_schema(
        request=TelegramChatIdSerializer,
        responses={200: TelegramChatIdSerializer},
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        request.user.telegram_chat_id = serializer.validated_data["telegram_chat_id"]
        request.user.save(update_fields=["telegram_chat_id"])

        return Response(
            {"telegram_chat_id": request.user.telegram_chat_id},
            status=status.HTTP_200_OK,
        )
