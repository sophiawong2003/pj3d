from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.video_summary, name='video_list'),
    path('search/', views.video_summary, name='video_search'),
    path('category/<int:category_id>/', views.video_summary, name='category_view'),
    path('<int:pk>/', views.video_player, name='video_player'),
    path('<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('dashboard/', views.favorite_dashboard, name='favorite_dashboard'),
]