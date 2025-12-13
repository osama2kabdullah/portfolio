from django.shortcuts import render
from portfolio.models import Project, Skill
from blog.models import Post


def home(request):
    projects = Project.objects.filter(published=True).order_by("-created")[:6]
    skills = Skill.objects.order_by("-level")[:12]
    posts = Post.objects.filter(published=True).order_by("-created")[:3]
    return render(request, "core/home.html", {"projects": projects, "skills": skills, "posts": posts})
