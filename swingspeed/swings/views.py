from .models import User
from .serializers import SwingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Swing

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
    def get(self, request, format=None):
        swings = Swing.objects.all()
        serializer = SwingSerializer(swings, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SwingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SwingDetail(APIView):
    """
    Retrieve, update or delete a swing instance.
    """
    def get_object(self, pk):
        try:
            return Swing.objects.get(pk=pk)
        except Swing.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        swing = self.get_object(pk)
        serializer = SwingSerializer(swing)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        swing = self.get_object(pk)
        serializer = SwingSerializer(swing, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        swing = self.get_object(pk)
        swing.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)