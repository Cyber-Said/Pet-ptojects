from django.db.migrations import serializer
from django.forms import model_to_dict
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PlaylistSerializer
from .models import Playlist


# Create your views here.
class PlaylistView(APIView):
    def get(self,request):
        playlists = Playlist.objects.all().values()
        return Response({'playlists':PlaylistSerializer(playlists, many=True).data})

    def post(self,request):
        serializer = PlaylistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'created_status': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({'error': 'Playlist ID not found'})
        try:
            playlist = Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            return Response({'error': 'Playlist not found'})

        serializer = PlaylistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'updated_status': serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"ERROR": "Delete Method Is Not Allowed"})
        try:
            instance = Playlist.objects.get(pk=pk)
            instance.delete()
        except Playlist.DoesNotExist:
            return Response({"ERROR": "Object Not Found !"})

        return Response({"post": f"Object {str(pk)} is deleted"})
