from rest_framework import serializers
from .models import Tag, VideoTag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class VideoTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoTag
        fields = '__all__'