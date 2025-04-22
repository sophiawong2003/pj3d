from django.shortcuts import render

from courses.models import Course
from tutors.models import Tutor
from courses.choices import coursefee_choices, classsize_choices, topic_choices
# Create your views here.
def index(request):
    courses = Course.objects.order_by('-list_date').filter(is_published=True)[:3]
    context = {"courses": courses,
               "coursefee_choices" : coursefee_choices,
               "classsize_choices" : classsize_choices,
               "topic_choices" : topic_choices}
    return render(request, 'pages/index.html', context)

def about(request):
    tutors = Tutor.objects.order_by('-hire_date')
    mvp_tutors = Tutor.objects.all().filter(is_mvp=True)
    context = {"tutors" : tutors, "mvp_tutors" : mvp_tutors}
    return render(request, 'pages/about.html', context)
