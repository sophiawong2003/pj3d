from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'favorites_count')
    
    def favorites_count(self, obj):
        return obj.favorites.count()

admin.site.register(UserProfile, UserProfileAdmin)
