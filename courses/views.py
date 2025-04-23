from django.shortcuts import render, get_object_or_404
from . models import Course    # . means from same level
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, F
from courses.choices import coursefee_choices, classsize_choices, topic_choices

# Create your views here.
def courses(request):
    # courses = Course.objects.filter(district= F('address'))
    courses = Course.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(courses, 3)  #based on class Paginator, 3 in a group
    page = request.GET.get('page')
    paged_courses = paginator.get_page(page)
    context = {'courses' : paged_courses}    #variables wrapped under context
    return render(request, 'courses/courses.html', context) #pass address of context to template engine

def course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    context = {'course' : course}
    return render(request, 'courses/course.html', context)

def search(request):
    queryset_list = Course.objects.select_related('tutor').order_by('-list_date').filter(is_published=True).only(
        'id', 'title', 'coursecode', 'coursefee', 'classsize', 'photo_main', 'list_date', 'tutor__name'
    )
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)
    if 'title' in request.GET:
        title = request.GET['title']
        if title:
            queryset_list = queryset_list.filter(title__icontains=title)
    if 'topic' in request.GET:
        topic = request.GET['topic']
        if topic:
            queryset_list = queryset_list.filter(topic__iexact=topic)
    if 'coursefee' in request.GET:
        coursefee = request.GET['coursefee']
        if coursefee:
            queryset_list = queryset_list.filter(coursefee__lte=coursefee)
    if 'coursecode' in request.GET:
        coursecode = request.GET['coursecode']
        if coursecode:
            queryset_list = queryset_list.filter(coursecode__lte=coursecode)
    paginator = Paginator(queryset_list, 3)  #based on class Paginator, 3 in a group
    page = request.GET.get('page')
    paged_courses = paginator.get_page(page)
    values = request.GET.copy()
    if 'page' in values:
        del values["page"]
    context = {
        'coursefee_choices' : coursefee_choices,
        'topic_choices' : topic_choices,
        'classsize_choices' : classsize_choices,
        'courses' : paged_courses,
        'values' : values
    }
    return render(request, 'courses/search.html', context)
