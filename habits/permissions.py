from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        return obj.user == request.user


class PublicReadOnly(BasePermission):
    """
    Публичные привычки доступны всем только на чтение.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in SAFE_METHODS and obj.is_public:
            return True
        return False
