from django.contrib import admin

from Videos.models import Video, Comment

# Register your models here.
admin.site.register(Video)
admin.site.register(Comment)