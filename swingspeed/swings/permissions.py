from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view/edit
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'PUT', 'DELETE'):
            return obj.user.pk == request.user.pk
        return False

    