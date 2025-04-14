from django.urls import path #from module import function
from . import views   #from current folder import file

urlpatterns = [
    path('',views.index, name='index'), #if endpt empty, run index function in file-views
    path('about', views.about, name='about'),
]