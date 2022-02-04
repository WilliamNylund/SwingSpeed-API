from .serializers import SwingSerializer, SwingUpdateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Swing
from rest_framework.authentication import TokenAuthentication
from swings.permissions import IsOwnerOrAdmin
from rest_framework import permissions
from .videoanalysis import analyze
import time
import threading

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
        request.data['user'] = request.user.pk
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

"""
    Upload a swing for measuring (WIP)
"""
class SwingMeasurment(APIView):
    def post(self, request, format=None):
        print("video upload request recieved")
        start = time.time()
        video = request.FILES.get('video', None)
        if video is None:
            print("video was not provided")
            return Response('Video was not provided', status=status.HTTP_400_BAD_REQUEST)
        path = video.temporary_file_path()

        #Start a thread that does the video analysis
        print('starting thread')
        thread = threading.Thread(target=analyze, args=(path,))
        thread.start()
        end = time.time()
        print('request done in: ' + str(end - start))
        
        return Response('result', status=status.HTTP_200_OK)

"""
4.MOV 4.20MB
LOCAL: 0.37s analysis, 0.43 total
HEROKU: 1.31s analysis, 2.3 total

golf.mp4 22.5MB
LOCAL: 3.64s analysis, 3.82 total
HEROKU: 8.38s analysis, 9.24 total

3.mp4 39.3MB
LOCAL: 4.33s analysis, 4.62 total
HEROKU: 9.73s analysis, 12.19 total

videoplayback.mp4 22.5MB 
LOCAL: 4s
HEROKU: Sometimes 20s sometimes  7s??

with mask: 22.5MB
LOCAL: 47.0s twice
HEROKU: times out after 30 seconds

with mask: 4.2MB
LOCAL: 5s
HEROKU: times out after 30 seconds
"""