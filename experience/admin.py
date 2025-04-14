from django.contrib import admin
from .models import TimelineEvent, Video

@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'event_type', 'date_created')
    list_filter = ('event_type', 'event_date')
    search_fields = ('title', 'description')
    ordering = ('-event_date',)
    fieldsets = (
        (None, {
            'fields': ('title', 'event_type', 'description', 'event_date')
        }),
        ('Media', {
            'fields': ('main_photo', 'photo_1', 'photo_2', 'photo_3', 
                      'photo_4', 'photo_5', 'photo_6', 'social_link')
        }),
    )

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_created')
    search_fields = ('title', 'description')
    ordering = ('-date_created',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description')
        }),
        ('Media', {
            'fields': ('video_file',)
        }),
    )
