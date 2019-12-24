from django.contrib import admin
from .models import Video

TEXT_TO_STATE = {
    k[1]: k[0]
    for k in Video.STATE_CHOICES
}

class VideoAdmin(admin.ModelAdmin):
    list_display = ('video_name', 'video_class', 'state', 'cut_points')
    search_fields = ('video_name', 'video_class', 'state')

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(VideoAdmin, self).get_search_results(request, queryset, search_term)
        if search_term in TEXT_TO_STATE:
            queryset |= self.model.objects.filter(state=TEXT_TO_STATE[search_term])
        return queryset, use_distinct

admin.site.register(Video, VideoAdmin)
# Register your models here.
