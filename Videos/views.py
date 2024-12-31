from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import VideoSerializer, CommentSerializer
from .models import Video, Comment

from .utils import *

# class VideoPagination(PageNumberPagination):
#     page_size = 12  # Пагинация по 12 видео

class VideoView(APIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]

    # permission_classes = [AllowAny]


    # def get(self, request):
    #     videos = Video.objects.all()
    #
    #     paginator = VideoPagination()
    #     result_page = paginator.paginate_queryset(videos, request)
    #     serializer = VideoSerializer(result_page, many=True)
    #
    #     # Возвращаем пагинированный ответ
    #     return paginator.get_paginated_response(serializer.data)

    def get(self, request):

        videos, search_query = searchVideos(request)
        # for i in range(19): print('dfgh')
        paginated_data = paginatVideos(request, videos)

        serializer = VideoSerializer(paginated_data["video"], many=True)
        return Response({
            "video": serializer.data,
            "current_page": request.GET.get('page', 1),
            "search_query": search_query,
            "total_videos": len(videos),
        })

    @swagger_auto_schema(
        request_body=VideoSerializer,
        responses={201: VideoSerializer},
    )
    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'created_status': serializer.data})

    @swagger_auto_schema(
        request_body=CommentSerializer,
        responses={201: CommentSerializer},
    )
    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({'error': 'Video ID not found'})
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response({'error': 'Video not found'})

        serializer = VideoSerializer(video, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'updated_status': serializer.data})


    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"ERROR": "Delete Method Is Not Allowed"})
        try:
            instance = Video.objects.get(pk=pk)
            instance.delete()
        except Video.DoesNotExist:
            return Response({"ERROR": "Object Not Found !"})

        return Response({"post": f"Object {str(pk)} is deleted"})
class CommentView(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # permission_classes = [AllowAny]

    def get(self, request):
        comment = Comment.objects.all()
        return Response({'Comments': CommentSerializer(comment, many=True).data})

    @swagger_auto_schema(
        request_body=CommentSerializer,
        responses={201: CommentSerializer},
    )
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'created_status': serializer.data})

    @swagger_auto_schema(
        request_body=CommentSerializer,
        responses={201: CommentSerializer},
    )
    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({'error': 'Comment ID not found'})
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'})

        serializer = CommentSerializer(comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'updated_status': serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"ERROR": "Delete Method Is Not Allowed"})
        try:
            instance = Comment.objects.get(pk=pk)
            instance.delete()
        except Comment.DoesNotExist:
            return Response({"ERROR": "Object Not Found !"})

        return Response({"post": f"Object {str(pk)} is deleted"})

class VideoDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        try:
            video = Video.objects.get(pk=id)
        except Video.DoesNotExist:
            return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = VideoSerializer(video)
        return Response(serializer.data, status=status.HTTP_200_OK)