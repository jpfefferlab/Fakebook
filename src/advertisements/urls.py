from django.urls import path
from .views import click_ad

app_name = 'advertisements'

urlpatterns = [
    path('<pk>', click_ad, name='click-ad'),
]