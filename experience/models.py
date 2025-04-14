from django.db import models
from django.utils import timezone

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    video_thumbnail = models.ImageField(upload_to='experience/making_video/thumbnails/', blank=True, null=True)
    youtube_link = models.URLField(max_length=500)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_created']

class TimelineEvent(models.Model):
    EVENT_TYPES = [
        ('exhibition', '展覽'),
        ('competition', '比賽'),
        ('workshop', '工作坊及作品製作'),
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
    
    def get_icon(self):
        """Returns the appropriate Font Awesome icon class based on event type"""
        icon_mapping = {
            'exhibition': 'fas fa-camera-retro',
            'competition': 'fas fa-trophy',
            'workshop': 'fas fa-chalkboard-teacher'
        }
        return icon_mapping.get(self.event_type, 'fas fa-calendar')  # default icon

    def get_colors(self):
        """Returns the color variables based on event type"""
        color_mapping = {
            'exhibition': {
                'bg': 'var(--color1)',    # Purple
                'text': 'var(--color2)'    # Light purple
            },
            'competition': {
                'bg': 'var(--color4)',     # Blue
                'text': 'var(--color3)'    # Light blue
            },
            'workshop': {
                'bg': 'var(--color5)',     # Green
                'text': 'var(--color6)'    # Light green
            }
        }
        return color_mapping.get(self.event_type, {'bg': 'var(--color1)', 'text': 'var(--color2)'})

  
    class Meta:
        ordering = ['event_date']
