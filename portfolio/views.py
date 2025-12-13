from django.shortcuts import render, get_object_or_404
from .models import Project, Skill


def project_list(request):
    projects = Project.objects.filter(published=True).order_by("-created")
    return render(request, "portfolio/project_list.html", {"projects": projects})


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, published=True)
    return render(request, "portfolio/project_detail.html", {"project": project})
