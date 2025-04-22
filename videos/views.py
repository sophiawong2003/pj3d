from django.shortcuts import render, get_object_or_404, redirect
from .models import Video, Category
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile

def video_summary(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    
    videos = Video.objects.select_related('category').annotate(
        view_count=Count('views')).order_by('-created_at')
    categories = Category.objects.annotate(video_count=Count('video'))
    
    if query:
        videos = videos.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
        
    if category_id:
        videos = videos.filter(category__id=category_id)
    
    context = {
        'videos': videos,
        'categories': categories,
        'current_category': int(category_id) if category_id else None,
        'search_query': query or ''
    }
    return render(request, 'videos/summary.html', context)

def video_player(request, pk):
    video = get_object_or_404(Video.objects.select_related('category'), pk=pk)
    video.views += 1
    video.save()
    
    # Get related videos from the same category
    related_videos = video.category.video_set.exclude(pk=pk).order_by('-created_at')[:3]
    
    # Check if video is in user's favorites
    is_favorite = False
    if request.user.is_authenticated and hasattr(request.user, 'userprofile'):
        is_favorite = request.user.userprofile.favorites.filter(pk=video.pk).exists()
    
    return render(request, 'videos/player.html', {
        'video': video,
        'related_videos': related_videos,
        'is_favorite': is_favorite
    })

@login_required
def toggle_favorite(request, pk):
    video = get_object_or_404(Video, pk=pk)
    profile = request.user.userprofile
    
    if profile.favorites.filter(pk=video.pk).exists():
        profile.favorites.remove(video)
    else:
        profile.favorites.add(video)
    
    return redirect('videos:video_player', pk=video.pk)

@login_required
def favorite_dashboard(request):
    favorite_videos = request.user.userprofile.favorites.all()
    return render(request, 'videos/dashboard.html', {
        'favorite_videos': favorite_videos
    })
