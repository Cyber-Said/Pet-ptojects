from django.contrib import admin

from Playlists.models import Playlist, VideoPlaylist

# Register your models here.
admin.site.register(Playlist)
admin.site.register(VideoPlaylist)
