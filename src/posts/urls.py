from django.urls import path
from .views import PostDeleteView, PostUpdateView, post_comment_create_and_list_view, like_unlike_post, dislike_undislike_post, report_unreport_post

app_name = 'posts'

urlpatterns = [
    path('', post_comment_create_and_list_view, name='main-post-view'),
    path('liked/', like_unlike_post, name='like-post-view'),
    path('disliked/', dislike_undislike_post, name='dislike-post-view'),
    path('reported/', report_unreport_post, name='report-post-view'),
    path('<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<pk>/update/', PostUpdateView.as_view(), name='post-update'),

]