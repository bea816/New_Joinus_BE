from rest_framework import permissions

# 유저와 유저의 토큰이 맞는지 확인
class CustomReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user