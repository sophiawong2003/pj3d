from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=200)
    youtube_url = models.URLField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
        
    def get_youtube_id(self):
        """Extracts YouTube ID from URL"""
        if 'youtu.be/' in self.youtube_url:
            return self.youtube_url.split('youtu.be/')[-1]
        return self.youtube_url.split('v=')[-1].split('&')[0]

