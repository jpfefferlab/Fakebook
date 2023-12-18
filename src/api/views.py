import datetime
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from advertisements.models import Advertisement
from api.forms import APIPostModelForm, APIProfileModelForm, APIAdvertisementModelForm
from configuration.models import get_the_config
from posts.models import Post, PlannedReaction
from profiles.models import Profile, Relationship

from django.contrib.auth.models import User


@csrf_exempt
def create_user(request):
    if not verify_token(request):
        return HttpResponse(content="401 Unauthorized", status=401)

    if request.method != "POST":
        return HttpResponse(content="405 Method Not Allowed", status=405)

    username = request.GET.get("username", "")
    password = request.GET.get("password", "")
    email = request.GET.get("email", "")
    first_name = request.GET.get("firstName", "")
    last_name = request.GET.get("lastName", "")
    bio = request.GET.get("bio", "")
    country = request.GET.get("country", "")

    if username == "" or password == "" or email == "":
        return HttpResponse(content="400 Bad request", status=400)

    if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
        return HttpResponse(content="409 Conflict - username or email already in use", status=409)


    user = User.objects.create_user(username=username, email=email, password=password)
    # profile is automatically created by signal
    profile = Profile.objects.filter(user=user).first()

    if first_name != "":
        # user.first_name = first_name
        profile.first_name = first_name
    if last_name != "":
        # user.last_name = last_name
        profile.last_name = last_name
    if bio != "":
        profile.bio = bio
    if country != "":
        profile.country = country

    if request.FILES.get("avatar", None) is not None:
        form = APIProfileModelForm(request.POST, request.FILES)
        if not form.is_valid():
            return HttpResponse(content="400 Bad request - form is invalid", status=400)
        temp_profile = form.save(commit=False)
        profile.avatar = temp_profile.avatar

    user.save()
    profile.save()

    print(f"[API] Created user {username}")

    return json_response({
        "userId": user.id,
        "profileId": profile.id
    })

@csrf_exempt
def modify_relationship(request):
    if not verify_token(request):
        return HttpResponse(content="401 Unauthorized", status=401)

    if request.method != "POST" and request.method != "DELETE":
        return HttpResponse(content="405 Method Not Allowed", status=405)


    try:
        profile_id_1 = int(request.GET.get("profileId1", ""))
        profile_id_2 = int(request.GET.get("profileId2", ""))
    except ValueError:
        return HttpResponse(content="400 - Arguments must be integers", status=400)

    profile1 = Profile.objects.filter(id=profile_id_1).first()
    profile2 = Profile.objects.filter(id=profile_id_2).first()

    if profile1 is None or profile2 is None:
        return HttpResponse(content="404 Not Found", status=404)

    if request.method == "POST":
        relationship = Relationship.objects.filter(sender=profile2, receiver=profile1).first()
        if relationship is None:
            relationship, created = Relationship.objects.get_or_create(sender=profile1, receiver=profile2)
        relationship.status = "accepted"
        relationship.save()

        print(f"[API] Created relationship between {profile1.user.username} and {profile2.user.username}")

    elif request.method == "DELETE":
        relationship = Relationship.objects.filter(sender__in=[profile1, profile2], receiver__in=[profile1, profile2]).first()
        if relationship is None:
            return HttpResponse(content="404 Not Found", status=404)
        relationship.delete()

        print(f"[API] Deleted relationship between {profile1.user.username} and {profile2.user.username}")

    return HttpResponse(status=200)


@csrf_exempt
def create_delete_post(request):
    if not verify_token(request):
        return HttpResponse(content="401 Unauthorized", status=401)

    if request.method != "POST" and request.method != "DELETE":
        return HttpResponse(content="405 Method Not Allowed", status=405)

    if request.method == "POST":
        try:
            author_id = int(request.GET.get("profileId", ""))
            created_string = request.GET.get("created", "")
            if created_string != "":
                created = datetime.datetime.fromtimestamp(float(created_string))
            else:
                created = datetime.datetime.now()
        except ValueError:
            return HttpResponse(content="400 Bad request - Invalid parameters", status=400)

        content = request.GET.get("content", "")

        author = Profile.objects.filter(id=author_id).first()

        if author is None:
            return HttpResponse(content="404 Not Found", status=404)

        if request.FILES.get("image", None) is not None:
            form = APIPostModelForm(request.POST, request.FILES)
            if not form.is_valid():
                return HttpResponse(content="400 Bad request - form is invalid", status=400)
            post = form.save(commit=False)
            post.author = author
            post.created = created
            post.content = content
        else:
            post = Post.objects.create(author=author, created=created, content=content)

        post.save()

        post_id = post.id

        print(f"[API] Created post {post_id}")

        return json_response({
            "postId": post_id
        })

    elif request.method == "DELETE":
        try:
            post_id = int(request.GET.get("postId", ""))
        except ValueError:
            return HttpResponse(content="400 - postId must be integer", status=400)

        post = Post.objects.filter(id=post_id).first()

        if post is None:
            return HttpResponse(content="404 Not Found", status=404)

        post.delete()
        print(f"[API] Deleted post {post_id}")
        return HttpResponse(status=200)


@csrf_exempt
def create_delete_advertisement(request):
    if not verify_token(request):
        return HttpResponse(content="401 Unauthorized", status=401)

    if request.method != "POST" and request.method != "DELETE":
        return HttpResponse(content="405 Method Not Allowed", status=405)

    if request.method == "POST":
        text = request.GET.get("text", "")
        url = request.GET.get("url", "")

        if request.FILES.get("image", None) is None:
            return HttpResponse(content="400 - image is mandatory", status=400)

        form = APIAdvertisementModelForm(request.POST, request.FILES)
        if not form.is_valid():
            return HttpResponse(content="400 Bad request - form is invalid", status=400)

        advertisement = form.save(commit=False)
        advertisement.text = text
        advertisement.url = url
        advertisement.save()

        ad_id = advertisement.id

        print(f"[API] Created advertisement {ad_id}")

        return json_response({
            "adId": ad_id
        })

    elif request.method == "DELETE":
        try:
            ad_id = int(request.GET.get("adId", ""))
        except ValueError:
            return HttpResponse(content="400 - adId must be integer", status=400)

        ad = Advertisement.objects.filter(id=ad_id).first()

        if ad is None:
            return HttpResponse(content="404 Not Found", status=404)

        ad.delete()
        print(f"[API] Deleted advertisement {ad_id}")
        return HttpResponse(status=200)


@csrf_exempt
def modify_reaction(request):
    if not verify_token(request):
        return HttpResponse(content="401 Unauthorized", status=401)

    if request.method != "POST" and request.method != "DELETE":
        return HttpResponse(content="405 Method Not Allowed", status=405)

    if request.method == "POST":
        try:
            author_profile_id = int(request.GET.get("profileId", ""))
            time_delta = int(request.GET.get("timeDelta", "0"))
        except ValueError:
            return HttpResponse(content="400 - profileId and timeDelta must be integer", status=400)

        author_profile = Profile.objects.filter(id=author_profile_id).first()
        if author_profile is None:
            return HttpResponse(content="404 Not Found - author profile not found", status=404)

        reaction_type = request.GET.get("type", "")
        if not reaction_type in ["Like", "Dislike"]:
            return HttpResponse(content="400 - type must be in ['Like', 'Dislike']", status=400)

        post_id_string = request.GET.get("postId", "")

        if post_id_string != "":
            try:
                post_id = int(post_id_string)
            except ValueError:
                return HttpResponse(content="400 - postId must be integer", status=400)

            post = Post.objects.filter(id=post_id).first()
            if post is None:
                return HttpResponse(content="404 Not Found - post not found", status=404)

            planned_reaction = PlannedReaction.objects.create(user=author_profile, time_delta=time_delta,
                                                              reaction_type=reaction_type, post=post)
            planned_reaction_id = planned_reaction.id
            print(f"[API] Created planned reaction {planned_reaction_id}")

            return json_response({
                "plannedReactionId": planned_reaction_id
            })

        else:
            try:
                target_profile_id = int(request.GET.get("targetProfileId", ""))
                post_offset = int(request.GET.get("postOffset", ""))
            except ValueError:
                return HttpResponse(content="400 - targetProfileId and postOffset must be integer", status=400)

            target_profile = Profile.objects.filter(id=target_profile_id).first()
            if target_profile is None:
                return HttpResponse(content="404 Not Found - target profile not found", status=404)

            planned_reaction = PlannedReaction.objects.create(user=author_profile, time_delta=time_delta,
                                                              reaction_type=reaction_type,
                                                              target_profile=target_profile, post_offset=post_offset)
            planned_reaction_id = planned_reaction.id
            print(f"[API] Created planned reaction {planned_reaction_id}")

            return json_response({
                "plannedReactionId": planned_reaction_id
            })

    elif request.method == "DELETE":
        try:
            reaction_id = int(request.GET.get("reactionId", ""))
        except ValueError:
            return HttpResponse(content="400 - reactionId must be integer", status=400)

        planned_reaction = PlannedReaction.objects.filter(id=reaction_id).first()

        if planned_reaction is None:
            return HttpResponse(content="404 Not Found", status=404)

        planned_reaction.delete()
        print(f"[API] Deleted reaction {reaction_id}")
        return HttpResponse(status=200)


def json_response(data):
    return HttpResponse(content=json.dumps(data), content_type="application/json", status=200)

def verify_token(request):
    return request.headers.get("Token", "") == get_the_config().management_token

