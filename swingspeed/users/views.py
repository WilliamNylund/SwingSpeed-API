from .models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from users.permissions import IsOwnerOrAdmin

"""
    THIS VIEW IS CURRENTLY NOT IN USE, AS WERE USING DJOSER VIEWS
"""

class UserList(APIView):
    """
    List all users, or create a new user.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    def get_object(self, pk):
        try:
            obj = User.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)