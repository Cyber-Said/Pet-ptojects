from django.contrib import admin

from Tags.models import Tag, VideoTag

# Register your models here.
admin.site.register(Tag)
admin.site.register(VideoTag)