from django.shortcuts import render, get_object_or_404
from .models import TimelineEvent, Video
from django.views.generic import DetailView

def experience_view(request):
    timeline_events = TimelineEvent.objects.all().order_by('event_date')
    return render(request, 'experience/experience.html', {
        'timeline_events': timeline_events
    })

def making_video(request):
    videos = Video.objects.all()
    return render(request, 'experience/making_video.html', {'videos': videos})

class EventDetailView(DetailView):
    model = TimelineEvent
    template_name = 'experience/event_detail.html'
    context_object_name = 'event'
