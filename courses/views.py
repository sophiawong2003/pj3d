from django.shortcuts import render, get_object_or_404
from . models import Course    # . means from same level
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, F
# from courses.choices import price_choices, bedroom_choices, district_choices

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
    course = get_object_or_404(course, pk=course_id)
    context = {'course' : course}
    return render(request, 'courses/course.html', context)

def search(request):
    queryset_list = Course.objects.order_by('-list_date').filter(is_published=True)
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)
    if 'title' in request.GET:
        title = request.GET['title']
        if title:
            queryset_list = queryset_list.filter(title__icontains=title)
    if 'district' in request.GET:
        district = request.GET['district']
        if district:
            queryset_list = queryset_list.filter(district__iexact=district)
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)
    paginator = Paginator(queryset_list, 3)  #based on class Paginator, 3 in a group
    page = request.GET.get('page')
    paged_courses = paginator.get_page(page)
    values = request.GET.copy()
    if 'page' in values:
        del values["page"]
    context = {
        # 'price_choices' : price_choices,
        # 'district_choices' : district_choices,
        # 'bedroom_choices' : bedroom_choices,
        'courses' : paged_courses,
        'values' : values
    }
    return render(request, 'courses/search.html', context)
