from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from Videos.serializers import VideoSerializer
from .serializers import TagSerializer, VideoTagSerializer
from .models import Tag, VideoTag


class TagView(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    permission_classes = [AllowAny]

    def get(self, request):
        Tags = Tag.objects.all()
        return Response({'Tags': TagSerializer(Tags, many=True).data})

    @swagger_auto_schema(
        request_serializer=TagSerializer,
        responses={201: TagSerializer},
    )
    def post(self, request):
        serializer = TagSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'created_status': serializer.data})

    @swagger_auto_schema(
        request_serializer=TagSerializer,
        responses={201: TagSerializer},
    )
    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({'error': 'Tag ID not found'})
        try:
            tag = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return Response({'error': 'Tag not found'})

        serializer = TagSerializer(tag, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'updated_status': serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"ERROR": "Delete Method Is Not Allowed"})
        try:
            instance = Tag.objects.get(pk=pk)
            instance.delete()
        except Tag.DoesNotExist:
            return Response({"ERROR": "Object Not Found !"})

        return Response({"post": f"Object {str(pk)} is deleted"})
class VideoTagView(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    permission_classes = [AllowAny]

    def get(self, request):
        video_Tags = VideoTag.objects.all()
        return Response({'video_tags': VideoTagSerializer(video_Tags, many=True).data})

    @swagger_auto_schema(
        request_serializer=VideoTagSerializer,
        responses={201: VideoTagSerializer},
    )
    def post(self, request):
        serializer = VideoTagSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'created_status': serializer.data})

    @swagger_auto_schema(
        request_serializer=VideoTagSerializer,
        responses={201: VideoTagSerializer},
    )
    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({'error': 'VideoTag ID not found'})
        try:
            video_Tag = VideoTag.objects.get(pk=pk)
        except VideoTag.DoesNotExist:
            return Response({'error': 'Tag not found'})

        serializer = VideoTagSerializer(video_Tag, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'updated_status': serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"ERROR": "Delete Method Is Not Allowed"})
        try:
            instance = VideoTag.objects.get(pk=pk)
            instance.delete()
        except VideoTag.DoesNotExist:
            return Response({"ERROR": "Object Not Found !"})

        return Response({"post": f"Object {str(pk)} is deleted"})

class TagVideos(APIView):
    permission_classes = [AllowAny]
    def get(self, request, id):
        try:
            # Получаем плейлист по ID
            tag = Tag.objects.get(pk=id)

            # Получаем все связи из VideoTag для данного плейлиста
            video_tags = VideoTag.objects.filter(tag=tag).select_related('video')

            # Извлекаем объекты видео
            videos = [vp.video for vp in video_tags]

            # Сериализуем список видео
            serializer = VideoSerializer(videos, many=True)

            # Возвращаем данные
            return Response({
                "tag": tag.name,
                "videos": serializer.data
            }, status=status.HTTP_200_OK)

        except Tag.DoesNotExist:
            return Response({"error": "Tag not found"}, status=status.HTTP_404_NOT_FOUND)
class TagDetailView(APIView):
    permission_classes = [AllowAny]  # Или IsAuthenticated, если доступ должен быть ограничен

    def get(self, request, id):
        try:
            # Получаем плейлист по ID
            tag = Tag.objects.get(pk=id)

            # Сериализуем объект плейлиста
            serializer = TagSerializer(tag)

            # Возвращаем данные
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Tag.DoesNotExist:
            return Response({"error": "Tag not found"}, status=status.HTTP_404_NOT_FOUND)
