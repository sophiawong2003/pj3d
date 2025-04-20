from django.contrib import admin
from .models import Video, Category

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'views', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('category', 'created_at')
    readonly_fields = ('views',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Video, VideoAdmin)
admin.site.register(Category, CategoryAdmin)
