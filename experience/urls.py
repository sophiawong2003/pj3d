from django.urls import path
from . import views

app_name = 'experience'

urlpatterns = [
    path('', views.experience_view, name='experience'),
    path('making_video/', views.making_video, name='making_video'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
]
