from django.shortcuts import render
from .models import Profile, AboutSettings

def about(request):
    profile = Profile.load()
    settings = AboutSettings.objects.first()
    return render(request, "about/about_me.html", {"profile": profile, "settings": settings,})