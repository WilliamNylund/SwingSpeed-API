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

"""
    Majority of user endpoints exist in Djoser
"""

class UserProfilePicture(APIView):
    """
    Profile picture handling
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

    def put(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            if user.profile_picture is not None:
                user.profile_picture.delete()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        user = self.get_object(request.user.id)
        serializer = UserProfilePictureSerializer(user)
        return Response(serializer.data)
        
    def delete(self, request, format=None):
        user = self.get_object(request.user.id)
        user.profile_picture.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)