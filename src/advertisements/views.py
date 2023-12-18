from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Advertisement
from profiles.models import Profile

@login_required
def click_ad(request, pk):
    user = request.user
    ad_obj = Advertisement.objects.get(id=pk)
    profile = Profile.objects.get(user=user)

    if profile not in ad_obj.user_clicked.all():
        ad_obj.user_clicked.add(profile)

    ad_obj.num_clicked += 1
    ad_obj.save()

    return redirect(ad_obj.url)

