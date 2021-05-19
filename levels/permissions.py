from rest_framework.permissions import BasePermission


class AdminPostPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return request.user.is_superuser and request.user.is_staff
