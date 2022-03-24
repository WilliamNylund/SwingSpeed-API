from cmath import e
from .serializers import SwingSerializer, SwingUpdateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Swing
from rest_framework.authentication import TokenAuthentication
from swings.permissions import IsOwnerOrAdmin
from rest_framework import permissions
from .tasks import test_task
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from os.path import exists
#TMP NOTE, soted user_1 recording swing id 17 kl 15:07
class SwingList(APIView):
    """
    List all swings, or create a new swing.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        swings = Swing.objects.all().filter(user=request.user, is_active=True)
        serializer = SwingSerializer(swings, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print("video upload request recieved")
        video = request.FILES.get('video', None)
        if video is None:
            return Response('Video was not provided', status=status.HTTP_400_BAD_REQUEST)
        print('video found, saving recording')
        swing = Swing(user=request.user, recording=video)
        swing.save()
        task = test_task.delay(swing.pk)
        # return task id for progress tracking
        return Response({'task_id': task.id}, status=status.HTTP_200_OK)

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
        serializer = SwingUpdateSerializer(swing, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        swing = self.get_object(pk)
        serializer = SwingUpdateSerializer(swing, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk, format=None):
        swing = self.get_object(pk)
        swing.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    

