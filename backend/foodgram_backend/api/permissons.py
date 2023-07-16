from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnlyPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_authenticated and obj.author == request.user


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user and request.user.is_staff)
