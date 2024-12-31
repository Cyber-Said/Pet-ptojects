
from Playlists.views import PlaylistView, VideoPlaylistView, PlaylistVideos, PlaylistDetailView
from Tags.views import TagView, VideoTagView, TagVideos, TagDetailView
from Videos.views import CommentView, VideoView, VideoDetailView
from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="FAQ Platform API",
        default_version='v1',
        description="API для Booking",
        contact=openapi.Contact(email="FAQ@mail.com"),
        license=openapi.License(name="Ala-Too License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
       path('admin/', admin.site.urls),
       path('api/v1/auth/', include('User.urls')),
       path('api/v1/playlist-list/', PlaylistView.as_view(), name='PlaylistView'),
       path('api/v1/playlist-list/<int:pk>', PlaylistView.as_view(), name='PlaylistView'),
       path('api/v1/video-playlist-list/', VideoPlaylistView.as_view(), name='VideoPlaylistView'),
       path('api/v1/video-playlist-list/<int:pk>', VideoPlaylistView.as_view(), name='VideoPlaylistView'),
       path('api/v1/tag-list/', TagView.as_view(), name='TagView'),
       path('api/v1/tag-list/<int:pk>', TagView.as_view(), name='TagView'),
       path('api/v1/video-tag-list/', VideoTagView.as_view(), name='VideoTagView'),
       path('api/v1/video-tag-list/<int:pk>', VideoTagView.as_view(), name='VideoTagView'),
       path('api/v1/video-list/', VideoView.as_view(), name='VideoView'),
       path('api/v1/video-list/<int:pk>', VideoView.as_view(), name='VideoView'),
       path('api/v1/comment-list/', CommentView.as_view(), name='CommentView'),
       path('api/v1/comment-list/<int:pk>', CommentView.as_view(), name='CommentView'),
       path('api/v1/playlist/<int:id>/videos/', PlaylistVideos.as_view(), name='Current-Playlist-Videos'),
       path('api/v1/videos/<int:id>/', VideoDetailView.as_view(), name='video-detail'),
       path('api/v1/playlist/<int:id>/',PlaylistDetailView.as_view(), name='playlist-detail'),
       path('api/v1/tag/<int:id>/videos/', TagVideos.as_view(), name='Current-Tag-Videos'),
       path('api/v1/tag/<int:id>/', TagDetailView.as_view(), name='tag-detail'),
       path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
