from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from portfolio_site.utils import render_thanks
from .models import Testimonial
from .forms import TestimonialSubmissionForm
from projects.models import Project
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from contact.models import ContactSettings

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
            testimonial = form.save()

            # =============================
            # EMAIL SETTINGS (shared logic)
            # =============================
            settings_obj = ContactSettings.objects.first()
            if settings_obj:
                sender_email = settings_obj.sender_email or settings.EMAIL_HOST_USER
                sender_name = settings_obj.sender_name or "Portfolio Website"
                recipient_email = settings_obj.recipient_email or settings.EMAIL_HOST_USER
            else:
                sender_email = settings.EMAIL_HOST_USER
                sender_name = "Portfolio Website"
                recipient_email = settings.EMAIL_HOST_USER

            # =============================
            # 1️⃣ ADMIN NOTIFICATION
            # =============================
            subject_admin = f"New Testimonial — {testimonial.project.title}" if testimonial.project else "New Testimonial Submitted"
            context_admin = {
                "testimonial": testimonial,
                "project": testimonial.project,
            }

            text_admin = render_to_string(
                "emails/testimonial_notification.txt", context_admin
            )
            html_admin = render_to_string(
                "emails/testimonial_notification.html", context_admin
            )

            email_admin = EmailMultiAlternatives(
                subject=subject_admin,
                body=text_admin,
                from_email=f"{sender_name} <{sender_email}>",
                to=[recipient_email],
                reply_to=[testimonial.email] if testimonial.email else None,
            )
            email_admin.attach_alternative(html_admin, "text/html")
            email_admin.send(fail_silently=False)

            # =============================
            # 2️⃣ AUTO-REPLY TO SUBMITTER
            # =============================
            if testimonial.email:
                subject_user = "Thank you for your testimonial!"
                context_user = {
                    "testimonial": testimonial,
                    "project": testimonial.project,
                }

                text_user = render_to_string(
                    "emails/testimonial_autoreply.txt", context_user
                )
                html_user = render_to_string(
                    "emails/testimonial_autoreply.html", context_user
                )

                email_user = EmailMultiAlternatives(
                    subject=subject_user,
                    body=text_user,
                    from_email=f"{sender_name} <{sender_email}>",
                    to=[testimonial.email],
                )
                email_user.attach_alternative(html_user, "text/html")
                email_user.send(fail_silently=False)

            # =============================
            # SESSION + REDIRECT (unchanged)
            # =============================
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
