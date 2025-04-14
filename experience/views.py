from django.shortcuts import render
from .models import TimelineEvent, Video

def experience_view(request):
    timeline_events = TimelineEvent.objects.all().order_by('event_date')
    return render(request, 'experience/experience.html', {
        'timeline_events': timeline_events
    })

def making_video(request):
    videos = Video.objects.all()
    return render(request, 'experience/making_video.html', {'videos': videos})

def event_detail(request, pk):
    event = TimelineEvent.objects.get(pk=pk)
    return render(request, 'experience/event_detail.html', {'event': event})
