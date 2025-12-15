from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Project
from services.models import Service
from django.db.models import Count, Q


def project_list(request):
    qs = Project.objects.filter(published=True).order_by("-created")

    selected_service = request.GET.get("service")
    if selected_service:
        qs = qs.filter(services__slug=selected_service)

    paginator = Paginator(qs, 9)
    page_number = request.GET.get("page")
    projects = paginator.get_page(page_number)

    filters = Service.objects.filter(published=True).annotate(
        project_count=Count('projects', filter=Q(projects__published=True))
    ).order_by("title")

    return render(
        request,
        "portfolio/project_list.html",
        {
            "projects": projects,
            "filters": filters,
            "selected_service": selected_service,
        },
    )


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, published=True)
    return render(request, "portfolio/project_detail.html", {"project": project})
