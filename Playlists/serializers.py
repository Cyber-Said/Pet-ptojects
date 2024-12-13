import io
from datetime import datetime

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Playlist, VideoPlaylist


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'

class VideoPlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoPlaylist
        fields = '__all__'





# class PlaylistModel(serializers.ModelSerializer):
#     def __init__(self, title, description):
#         self.title = title
#         self.description = description

#
# class PlaylistSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=255)
#     description = serializers.CharField()
#     created_by = serializers.IntegerField()
#     created_at = serializers.DateTimeField(default=datetime.now)
#
#     def create(self, validated_data):
#         return Playlist.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.created_by = validated_data.get('created_by', instance.created_by)
#         instance.created_at = validated_data.get('created_at', instance.created_at)
#         instance.save()
#         return instance

# def encode():
#     model = PlaylistModel("PlayList", "PlayList description")
#     model_sr = PlaylistSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json, type(json), sep='\n')
#
# def decode():
#     stream = io.BytesIO(b'{"title":"Playlist","description":"PlayList description"}')
#     data = JSONParser().parse(stream)
#     serializer = PlaylistSerializer(data=data)
#     if serializer.is_valid():
#         print(serializer.validated_data)
