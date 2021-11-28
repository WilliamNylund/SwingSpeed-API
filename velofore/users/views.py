from rest_framework.serializers import Serializer
from .models import User
from .serializers import UserSerializer, UserProfilePictureSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from users.permissions import IsOwnerOrAdmin
from django.conf import settings

"""
    THIS VIEW IS CURRENTLY NOT IN USE, AS WERE USING DJOSER VIEWS
"""

class UserProfilePicture(APIView):
    """
    Profilepicture handling
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

    def post(self, request, format=None):
        try:
            user = request.user
            if user.profile_picture is not None:
                user.profile_picture.delete()
            user.profile_picture = request.data['picture']
            user.save()
            serializer = UserProfilePictureSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        user = self.get_object(request.user.id)
        serializer = UserProfilePictureSerializer(user)
        return Response(serializer.data)
        
    def delete(self, request, format=None):
        user = self.get_object(request.user.id)
        user.profile_picture.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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