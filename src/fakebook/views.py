from fakebook.downloads import get_xlsx_file_from_database, get_database, get_zip_file
from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from configuration.models import get_the_config

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages

from profiles.models import Profile

import json

def home_view(request):
    user = request.user
    hello = 'Hello World'

    context = {
        'user': user,
        'hello': hello,
    }

    # return render(request, 'main/home.html', context)
    return redirect('posts:main-post-view')

@user_passes_test(lambda u: u.is_superuser)
def user_creation_view(request):
    return render(request, 'admin/custom_create_user.html')

@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    if request.method != "POST":
        return HttpResponse(content="405 Method Not Allowed", status=405)

    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    email = request.POST.get("email", "")
    first_name = request.POST.get("firstname", "")
    last_name = request.POST.get("lastname", "")
    bio = request.POST.get("bio", "")
    country = request.POST.get("country", "")

    if username == "" or password == "" or email == "":
        # shouldn't happen, UI will require input, so it's fine to just return 400
        return HttpResponse(content="400 Bad request", status=400)

    if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
        messages.add_message(request, messages.ERROR, "Conflict detected - username or email already in use. No action was taken.")
        # return HttpResponse(content="409 Conflict - username or email already in use", status=409)
        return redirect('user-creation-view')


    user = User.objects.create_user(username=username, email=email, password=password)
    # profile is automatically created by signal
    profile = Profile.objects.filter(user=user).first()

    if first_name != "":
        profile.first_name = first_name
    if last_name != "":
        profile.last_name = last_name
    if bio != "":
        profile.bio = bio
    if country != "":
        profile.country = country

    # for profile image support, use API route
    # This is not supported here as the view is not a form and would therefore have to manually implement uploading images

    user.save()
    profile.save()

    messages.add_message(request, messages.SUCCESS, f"User with id {user.id} and profile {profile.id} created successfully!")

    return redirect('user-creation-view')

@user_passes_test(lambda u: u.is_superuser)
def download_view(request):
    return render(request, 'admin/download_database.html')

@user_passes_test(lambda u: u.is_superuser)
def download_xlsx(request):
    # check which checkboxes were ticked and get the related tables in an xlsx file
    tables = ["user", "friends", "chats", "posts", "comments", "likes", "dislikes", "reports", "advertisements", "sessions", "post-views"]
    selected_tables = []
    for entry in tables:
        if str(request.POST.get(entry)) == "on":
            selected_tables.append(entry)
    xlsx_file = get_xlsx_file_from_database(selected_tables)   
    return xlsx_file

@user_passes_test(lambda u: u.is_superuser)
def download_database(request):
    database = get_database()
    return database

@user_passes_test(lambda u: u.is_superuser)
def download_pictures(request):
    print(request.POST)
    # check which checkboxes were ticked and get the zip archives
    archives = ["posts", "profile_pictures", "advertisements"]
    selected_archives = []
    for entry in archives:
        if str(request.POST.get(entry)) == "on":
            selected_archives.append(entry)
    zip_file = get_zip_file(selected_archives)   
    return zip_file

@csrf_exempt
def is_registration_enabled(request):
    return json_response({
        "registration_enabled": get_the_config().registration_enabled
    })

def json_response(data):
    return HttpResponse(content=json.dumps(data), content_type="application/json", status=200)