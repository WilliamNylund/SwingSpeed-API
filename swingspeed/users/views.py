from .models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .managers import UserManager

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
"""
{
"username": "guest4",
"password": "guest4",
"email": "halaba@hotmail.com",
"is_active": false
}
"""

"""
testuser1
testuser1
6a17f72ee80fa68c3922a14957c8e409865e5d74
"""

class UserList(APIView):
    """
    List all users, or create a new user.
    """
    def get(self, request, format=None):
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        #register
        serializer = UserSerializer(data=request.data)
        print('registering')
        if serializer.is_valid():
            user = UserManager.create_user(serializer.Meta, **serializer.data)
            token = Token.objects.create(user=user)
            createdUserSerializer = UserSerializer(user)
            return Response({
                'user': createdUserSerializer.data,
                'token': token.key
                },
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserLogin(APIView):
    """
    Login user using username and password, returning a token
    """
    def post(self, request, format=None):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        serializer = UserSerializer(user)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            print(token)
            return Response({
                'user': serializer.data,
                'token': token.key
            },
            status=status.HTTP_200_OK)
        else:
            raise Http404
            

class UserLogout(APIView):
    """
    Logout user, removing the token
    """
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response('User logged out successfully')