from django.urls import path
from . import views
from .views import EventDetailView

app_name = 'experience'

urlpatterns = [
    path('', views.experience_view, name='experience'),
    path('making_video/', views.making_video, name='making_video'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
]
