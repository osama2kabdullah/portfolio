from django.shortcuts import render
from portfolio.models import Project, Skill
from blog.models import Post
from services.models import Service
from testimonials.models import Testimonial
from about_me.models import Profile

def home(request):
    profile = Profile.objects.filter(is_active=True).first()
    projects = Project.objects.filter(published=True).order_by("-created")[:6]
    project_count = Project.objects.count()
    skills = Skill.objects.order_by("-level")[:12]
    posts = Post.objects.filter(published=True).order_by("-created")[:3]
    services = Service.objects.filter(published=True).order_by("order")[:8]
    testimonials = Testimonial.objects.filter(approved=True, featured=True).order_by("-order")[:1]
    return render(request, "core/home.html", {"projects": projects, "project_count": project_count, "skills": skills, "posts": posts, "services": services, "testimonials": testimonials, "profile": profile})
