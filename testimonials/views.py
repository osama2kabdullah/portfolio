from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from portfolio_site.utils import render_thanks
from .models import Testimonial
from .forms import TestimonialSubmissionForm
from portfolio.models import Project


def testimonials_list(request):
    qs = Testimonial.objects.filter(approved=True).order_by("-featured", "order")
    paginator = Paginator(qs, 6)
    page = request.GET.get("page")
    items = paginator.get_page(page)
    return render(request, "testimonials/testimonial_list.html", {"testimonials": items})

def testimonial_submit(request):
    project = None
    project_slug = request.GET.get("project")

    if project_slug:
        project = get_object_or_404(Project, slug=project_slug, published=True)

    if request.method == "POST":
        form = TestimonialSubmissionForm(request.POST, project=project)
        if form.is_valid():
            saved_testimonial = form.save()
            request.session["testimonial_submitted"] = True

            if not project_slug:
                form_project = form.cleaned_data.get("project")
                if form_project:
                    project_slug = form_project.slug
                    request.session["project"] = project_slug

            if project_slug:
                return redirect(f"{reverse('testimonial_thanks')}?project={project_slug}")
            return redirect("testimonial_thanks")
    else:
        form = TestimonialSubmissionForm(project=project)

    return render(
        request,
        "testimonials/testimonial_submit.html",
        {"form": form, "project": project},
    )

def testimonial_thanks(request):
    project_slug = request.GET.get("project") or request.session.get("project")
    project = None
    if project_slug:
        project = get_object_or_404(Project, slug=project_slug, published=True)

    if request.session.get("project"):
        del request.session["project"]

    return render_thanks(
        request,
        session_key="testimonial_submitted",
        redirect_url="testimonials_list",
        extra_context={
            "show_footer_contact": False,
            "title": f"Thank You{f' – {project.title}' if project else ''}",
            "heading": "Thank You for Your Testimonial",
            "subheading": "Testimonial Received",
            "message": "Your testimonial has been received and will appear on the site after approval.",
            "project": project,
        },
    )
