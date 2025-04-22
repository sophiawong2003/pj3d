from django.contrib import admin
from .models import Video, Category

class VideoAdmin(admin.ModelAdmin):
    actions = ['delete_selected']
    list_editable = ('category',)
    list_display = ('title', 'category', 'views', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('category', 'created_at')
    readonly_fields = ('views',)

class CategoryAdmin(admin.ModelAdmin):
    actions = ['delete_selected']
    list_editable = ('name',)
    list_display = ('name',)
    list_display_links = None
    search_fields = ('name',)

admin.site.register(Video, VideoAdmin)
admin.site.register(Category, CategoryAdmin)
