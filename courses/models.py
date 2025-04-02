from django.db import models
from datetime import datetime
from tutors.models import Tutor
from . choices import title_choices

# Create your models here.
class Course(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.DO_NOTHING, default='')
    title = models.CharField(max_length=200, default='')
    coursecode = models.CharField(max_length=200, default='')
    # street = models.CharField(max_length=200)
    topic = models.CharField(max_length=50, choices=title_choices.items(), default='')
    description = models.TextField(blank=True)
    studentreq = models.TextField(blank=True)
    coursefee = models.IntegerField(default='')
    classsize = models.IntegerField(default='0.0')
    durationhr = models.DecimalField(max_digits=2, decimal_places=1, default='')
    demo = models.URLField(max_length=500, default='https://example.com')
    # clubhouse = models.IntegerField(default=0)
    # sqft = models.IntegerField()
    # estate_size = models.FloatField(default=0.0)
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(default=datetime.now, blank=True)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f"Course Title : {self.title}"


