from django.shortcuts import render
from .models import TimelineEvent, ProductVideo

def experience_timeline(request):
    events = TimelineEvent.objects.all().order_by('-event_date')
    return render(request, 'experience/experience.html', {'events': events})

def making_video(request):
    videos = ProductVideo.objects.select_related('timeline_event').all()
    return render(request, 'experience/making_video.html', {'videos': videos})
