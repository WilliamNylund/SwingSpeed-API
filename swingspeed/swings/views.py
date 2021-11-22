from .models import User
from .serializers import SwingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Swing
from rest_framework.authentication import TokenAuthentication
from swings.permissions import IsOwnerOrAdmin
from rest_framework import permissions
"""
{
"username": "guest4",
"password": "guest4",
"email": "halaba@hotmail.com",
"is_active": false
}
"""

class SwingList(APIView):
    """
    List all swings, or create a new swing.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        swings = Swing.objects.all().filter(user=request.user)
        serializer = SwingSerializer(swings, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        request.data._mutable = True
        request.data['user'] = request.user.pk
        request.data._mutable = False

        serializer = SwingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SwingDetail(APIView):
    """
    Retrieve, update or delete a swing instance.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_object(self, pk):
        try:
            obj = Swing.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Swing.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        swing = self.get_object(pk)
        serializer = SwingSerializer(swing)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        swing = self.get_object(pk)
        serializer = SwingSerializer(swing, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        swing = self.get_object(pk)
        swing.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)