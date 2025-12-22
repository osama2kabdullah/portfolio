from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Project
from services.models import Service
from django.db.models import Count, Q
from testimonials.models import Testimonial


def project_list(request):
    qs = Project.objects.filter(published=True).order_by("-created")
    total_projects_count = qs.count()

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
            "total_projects_count": total_projects_count,
        },
    )


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, published=True)

    sections = project.sections.all()

    testimonial = (
        Testimonial.objects
        .filter(project=project, approved=True)
        .order_by("-featured", "order")
        .first()
    )

    next_project = (
        Project.objects
        .filter(published=True)
        .exclude(id=project.id)
        .filter(created__gt=project.created)
        .order_by("created")
        .first()
    )

    if not next_project:
        next_project = (
            Project.objects
            .filter(published=True)
            .exclude(id=project.id)
            .order_by("created")
            .first()
        )

    return render(
        request,
        "portfolio/project_detail.html",
        {
            "project": project,
            "sections": sections,
            "testimonial": testimonial,
            "next_project": next_project,
        }
    )