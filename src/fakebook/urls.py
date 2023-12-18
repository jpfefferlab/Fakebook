"""fakebook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view, user_creation_view, create_user, download_view, download_xlsx, download_database, download_pictures, is_registration_enabled

from django.views.static import serve


urlpatterns = [
    # these are the manually added links to download the database and xslx file
    path('admin/download_view', download_view, name='download-view'),
    path('admin/download_xlsx', download_xlsx, name='download-xlsx'),
    path('admin/download_database', download_database, name='download-database'),
    path('admin/download_pictures', download_pictures, name='download-pictures'),

    # custom user + profile creation page
    path('admin/user_creation_view', user_creation_view, name='user-creation-view'),
    path('admin/create_user', create_user, name='create-user'),
    
    path('admin/', admin.site.urls),
    path('', home_view, name='home-view'),
    path('is_registration_enabled/', is_registration_enabled, name='is_registration_enabled'),
    path('accounts/', include('allauth.urls')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('analytics/', include('analytics.urls', namespace='analytics')),
    path('api/', include('api.urls', namespace='api')),
    path('advertisements/', include('advertisements.urls', namespace='advertisements')),

    # https://stackoverflow.com/questions/5836674/why-does-debug-false-setting-make-my-django-static-files-access-fail
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    # re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]

# Serve static and media files in debug mode
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

