from django.urls import path
from . import views

app_name = 'experience'

urlpatterns = [
    path('', views.experience_view, name='experience'),
    path('videos/', views.making_video, name='experience_videos'),
]
