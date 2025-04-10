"""
URL configuration for pj3d project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static
from django.conf import settings

# path with greater chance to run earlier, reduce response time
# 1st resources route to admin app, Django built in
urlpatterns = [
    path('', include('pages.urls')), 
    path('courses/', include('courses.urls')),
    path('experience/', include('experience.urls')),
    # path('accounts/', include('accounts.urls')),
    # path('contacts/', include('contacts.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + debug_toolbar_urls() #only for testing, can be deleted after deploy
