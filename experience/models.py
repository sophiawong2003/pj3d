from django.db import models
from django.utils import timezone

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    video_file = models.FileField(upload_to='experience/videos/')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_created']

class TimelineEvent(models.Model):
    EVENT_TYPES = [
        ('exhibition', 'Exhibition'),
        ('competition', 'Competition'),
        ('workshop', 'Workshop'),
    ]
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, default='workshop')
    main_photo = models.ImageField(upload_to='experience/photos/main/',blank=True, null=True)
    photo_1 = models.ImageField(upload_to='experience/photos/', blank=True, null=True)
    photo_2 = models.ImageField(upload_to='experience/photos/', blank=True, null=True)
    photo_3 = models.ImageField(upload_to='experience/photos/', blank=True, null=True)
    photo_4 = models.ImageField(upload_to='experience/photos/', blank=True, null=True)
    photo_5 = models.ImageField(upload_to='experience/photos/', blank=True, null=True)
    photo_6 = models.ImageField(upload_to='experience/photos/', blank=True, null=True)
    social_link = models.URLField(max_length=500, blank=True, null=True, help_text="YouTube/Instagram/Facebook URL")
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.event_date.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['event_date']
