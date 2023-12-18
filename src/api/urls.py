from django.urls import path
from .views import create_user, modify_relationship, create_delete_post, modify_reaction, create_delete_advertisement

app_name = "api"

urlpatterns = [
    path('user', create_user, name='create-user'),
    path('profile/relationship', modify_relationship, name='modify-relationship'),
    path('profile/post', create_delete_post, name='create-delete-post'),
    path('profile/post/reaction', modify_reaction, name='modify-reaction'),
    path('advertisement', create_delete_advertisement, name='create-delete-advertisement'),
]



