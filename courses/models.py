from django.db import models
from datetime import datetime
from tutors.models import Tutor
from . choices import topic_choices

# Create your models here.
class Course(models.Model):
    id = models.AutoField(primary_key=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.DO_NOTHING, null=True, blank=True)
    title = models.CharField(max_length=200, default='')
    coursecode = models.CharField(max_length=200, default='')
    topic = models.CharField(max_length=50, choices=topic_choices.items(), default='')
    description = models.TextField(blank=True)
    studentreq = models.TextField(blank=True)
    coursefee = models.IntegerField(default=0)
    classsize = models.IntegerField(default=0)
    durationhr = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    list_date = models.DateTimeField(default=datetime.now, blank=True)
    demo = models.URLField(max_length=500, default='https://example.com')
    is_published = models.BooleanField(default=True)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f"Course Title : {self.title}"


