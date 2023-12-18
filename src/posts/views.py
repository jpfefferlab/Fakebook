from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from configuration.models import get_the_config
from .models import Post, Like, Dislike, Report, PlannedReaction
from profiles.models import Profile
from advertisements.models import Advertisement
from .forms import PostModelForm, CommentModelForm
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils.translation import gettext as _
from django.utils import timezone

from django.db.models import Q

import time

# Create your views here.

@login_required
def post_comment_create_and_list_view(request):
    profile = Profile.objects.get(user=request.user)

    process_planned_reactions(profile)

    friend_users = profile.friends.all()
    friend_user_ids = [user.id for user in friend_users]
    friend_profile_ids = [Profile.objects.get(user=user).id for user in friend_users]
    friend_profile_ids.append(profile.id)

    if get_the_config().posts_friends_only:
        qs = Post.objects.filter(created__lt=timezone.now(), author_id__in=friend_profile_ids)
    else:
        qs = Post.objects.filter(created__lt=timezone.now())


    ads = Advertisement.objects.all()

    post_added = False

    p_form = PostModelForm()
    c_form = CommentModelForm()

    profile = Profile.objects.get(user=request.user)

    if 'submit_p_form' in request.POST:
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostModelForm()
            post_added = True

            return redirect('posts:main-post-view')  # avoids replying to the post and follows post/redirect/get pattern

    if 'submit_c_form' in request.POST:
        if not get_the_config().comments_enabled:
            return redirect('posts:main-post-view')

        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm()

            return redirect('posts:main-post-view')

    context= {
        'qs': qs,
        'profile' : profile,
        'p_form': p_form,
        'c_form': c_form,
        'post_added': post_added,
        'ads': ads,
        'show_all_posts': not get_the_config().posts_friends_only,
        'show_all_comments': not get_the_config().comments_friends_only,
        'show_comments': get_the_config().comments_enabled,
        'friend_user_ids': friend_user_ids
    }

    return render(request, 'posts/main.html', context)

@login_required
def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        toggle_like(profile, post)

    return redirect('posts:main-post-view')

@login_required
def dislike_undislike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        toggle_dislike(profile, post)

    return redirect('posts:main-post-view')


def toggle_like(profile, post):
    if profile in post.liked.all():
        post.liked.remove(profile)
    else:
        post.liked.add(profile)

    like, created = Like.objects.get_or_create(user=profile, post_id = post.id)

    if not created:
        if like.value == 'Like':
            like.value = 'Unlike'
        else:
            like.value = 'Like'

    else:
        like.value='Like'

    post.save()
    like.save()

def toggle_dislike(profile, post):
    if profile in post.disliked.all():
        post.disliked.remove(profile)
    else:
        post.disliked.add(profile)

    dislike, created = Dislike.objects.get_or_create(user=profile, post_id = post.id)

    if not created:
        if dislike.value == 'Dislike':
            dislike.value = 'Undislike'
        else:
            dislike.value = 'Dislike'

    else:
        dislike.value='Dislike'

    post.save()
    dislike.save()

@login_required
def report_unreport_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.reported.all():
            post_obj.reported.remove(profile)
        else:
            post_obj.reported.add(profile)

        report, created = Report.objects.get_or_create(user=profile, post_id = post_id)

        if not created:
            if report.value == 'Report':
                report.value = 'Unreport'
            else:
                report.value = 'Report'

        else:
            report.value='Report'

        post_obj.save()
        report.save()

    return redirect('posts:main-post-view')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/confirm_del.html'
    success_url = reverse_lazy('posts:main-post-view')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, _("post-delete-error-no-author"))
        return obj


class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostModelForm
    model = Post
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:main-post-view')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, _("post-update-error-no-author"))
            return super().form_invalid(form)


# PLANNED_REACTION_UPDATE_INTERVAL = 60
# last_planned_reactions_update = 0
def process_planned_reactions(target_profile):
    # global last_planned_reactions_update
    # if time.time() - last_planned_reactions_update < PLANNED_REACTION_UPDATE_INTERVAL:
    #     return
    #
    # last_planned_reactions_update = time.time()
    # print("Updating planned reactions at ", time.time()) # TODO: debug statement, remove

    # update likes targeting own profile or a friends profile
    possible_target_profiles = [f.profile.id for f in target_profile.friends.all()]
    possible_target_profiles.append(target_profile.id)

    executed_reactions = []
    for planned_reaction in PlannedReaction.objects.filter(Q(target_profile_id__in=possible_target_profiles) | Q(post__isnull=False)):
        post = None

        if planned_reaction.post is not None:
            post = planned_reaction.post

        if planned_reaction.target_profile is not None:
            target_profile_posts = Post.objects.filter(author_id=planned_reaction.target_profile.id).order_by('created')
            if len(target_profile_posts) > planned_reaction.post_offset:
                post = target_profile_posts[planned_reaction.post_offset]

        if post is not None:
            if time.time() - post.created.timestamp() > planned_reaction.time_delta:
                profile = planned_reaction.user

                if profile is not None:
                    print(f"Executing planned {planned_reaction.reaction_type} on post {post.id} as profile {profile.user.username}")
                    if planned_reaction.reaction_type == "Like":
                        toggle_like(profile, post)
                    elif planned_reaction.reaction_type == "Dislike":
                        toggle_dislike(profile, post)

                    executed_reactions.append(planned_reaction.id)

    for to_be_removed in executed_reactions:
        PlannedReaction.objects.filter(id=to_be_removed).delete()

    print("Planned reactions left: ", PlannedReaction.objects.count())

