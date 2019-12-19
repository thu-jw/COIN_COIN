from django.contrib import admin
from .models import Video


class VideoAdmin(admin.ModelAdmin):
    list_display = ('video_name', 'video_class', 'state', 'cut_points')
    search_fields = ('video_name', 'video_class', 'state')

admin.site.register(Video, VideoAdmin)
# Register your models here.
