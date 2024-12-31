from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from Videos.serializers import VideoSerializer
from .serializers import PlaylistSerializer, VideoPlaylistSerializer
from .models import Playlist, VideoPlaylist


class PlaylistView(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # permission_classes = [AllowAny]

    def get(self, request):
        playlists = Playlist.objects.all()
        return Response({'playlists': PlaylistSerializer(playlists, many=True).data})

    @swagger_auto_schema(
        request_body=PlaylistSerializer,
        responses={201: PlaylistSerializer}
    )
    def post(self, request):
        serializer = PlaylistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)

        return Response({'created_status': serializer.data})

    @swagger_auto_schema(
        request_body=PlaylistSerializer,
        responses={201: PlaylistSerializer}
    )
    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({'error': 'Playlist ID not found'})
        try:
            playlist = Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            return Response({'error': 'Playlist not found'})

        serializer = PlaylistSerializer(playlist, data=request.data)
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
class VideoPlaylistView(APIView):

    # authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # permission_classes = [AllowAny]

    def get(self, request):
        video_playlists = VideoPlaylist.objects.all()
        return Response({'video_playlists': VideoPlaylistSerializer(video_playlists, many=True).data})

    @swagger_auto_schema(
        request_body=VideoPlaylistSerializer,
        responses={201: VideoPlaylistSerializer}
    )
    def post(self, request):
        serializer = VideoPlaylistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'created_status': serializer.data})

    @swagger_auto_schema(
        request_body=VideoPlaylistSerializer,
        responses={201: VideoPlaylistSerializer}
    )
    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({'error': 'VideoPlaylist ID not found'})
        try:
            video_playlist = VideoPlaylist.objects.get(pk=pk)
        except VideoPlaylist.DoesNotExist:
            return Response({'error': 'Playlist not found'})

        serializer = VideoPlaylistSerializer(video_playlist, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'updated_status': serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"ERROR": "Delete Method Is Not Allowed"})
        try:
            instance = VideoPlaylist.objects.get(pk=pk)
            instance.delete()
        except VideoPlaylist.DoesNotExist:
            return Response({"ERROR": "Object Not Found !"})

        return Response({"post": f"Object {str(pk)} is deleted"})
class PlaylistVideos(APIView):
    permission_classes = [AllowAny]
    def get(self, request, id):
        try:
            # Получаем плейлист по ID
            playlist = Playlist.objects.get(pk=id)

            # Получаем все связи из VideoPlaylist для данного плейлиста
            video_playlists = VideoPlaylist.objects.filter(playlist=playlist).select_related('video')

            # Извлекаем объекты видео
            videos = [vp.video for vp in video_playlists]

            # Сериализуем список видео
            serializer = VideoSerializer(videos, many=True)

            # Возвращаем данные
            return Response({
                "playlist": playlist.title,
                "videos": serializer.data
            }, status=status.HTTP_200_OK)

        except Playlist.DoesNotExist:
            return Response({"error": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND)
class PlaylistDetailView(APIView):
    permission_classes = [AllowAny]  # Или IsAuthenticated, если доступ должен быть ограничен

    def get(self, request, id):
        try:
            # Получаем плейлист по ID
            playlist = Playlist.objects.get(pk=id)

            # Сериализуем объект плейлиста
            serializer = PlaylistSerializer(playlist)

            # Возвращаем данные
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Playlist.DoesNotExist:
            return Response({"error": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND)
