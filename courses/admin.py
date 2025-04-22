from django.contrib import admin
from django.forms import NumberInput
from django.db import models

# Register your models here.

from .models import Course     #from models.py file under same directory import class
class CourseAdmin(admin.ModelAdmin):
    list_display=('id', 'title', 'is_published', 'tutor', 'coursefee', 'list_date', 'coursecode')
    list_display_links = 'id', 'title'     #multiple tuple no need to add comma
    list_filter = 'tutor',               #single tuple must add comma
    list_editable = 'is_published', 'coursefee', 'coursecode', 'tutor',
    search_fields = 'title', 'description', 'address', 'coursefee', 'tutor', 'coursecode'
    list_per_page = 25
    ordering = ['id']
    formfield_overrides = {
        models.IntegerField:{'widget': NumberInput (attrs={'size' : '10'})},}
    

admin.site.register(Course, CourseAdmin)    #in admin. register class(Course)
