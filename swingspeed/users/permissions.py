from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view/edit
    """
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'PUT', 'DELETE'):
            return obj.pk == request.user.pk
        return False

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view/edit
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'PUT', 'DELETE'):
            return (obj.pk == request.user.pk) or (request.user.is_staff)
        return False

    

    

    