from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from portfolio.models import Project, Skill
from blog.models import Post
from contact.models import Message
from core.models import SiteSettings
from .forms import ProjectForm, PostForm, SkillForm, MessageForm, SiteSettingsForm
from testimonials.models import Testimonial
from services.models import Service


@staff_member_required
def index(request):
    counts = {
        "projects": Project.objects.count(),
        "skills": Skill.objects.count(),
        "posts": Post.objects.count(),
        "messages": Message.objects.count(),
        "unread_messages": Message.objects.filter(is_read=False).count(),
    }
    recent_messages = Message.objects.order_by("-created")[:6]
    return render(request, "dashboard/index.html", {"counts": counts, "recent_messages": recent_messages})


def staff_required_view(fn):
    return staff_member_required(fn)


@staff_member_required
def projects_list(request):
    projects = Project.objects.order_by("-created")
    return render(request, "dashboard/projects_list.html", {"projects": projects})


@staff_member_required
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard_projects")
    else:
        form = ProjectForm()
    return render(request, "dashboard/project_form.html", {"form": form})


@staff_member_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("dashboard_projects")
    else:
        form = ProjectForm(instance=project)
    return render(request, "dashboard/project_form.html", {"form": form, "project": project})


@staff_member_required
def posts_list(request):
    posts = Post.objects.order_by("-created")
    return render(request, "dashboard/posts_list.html", {"posts": posts})


@staff_member_required
def messages_list(request):
    messages = Message.objects.order_by("-created")
    return render(request, "dashboard/messages_list.html", {"messages": messages})


@staff_member_required
def message_view(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    if request.method == "POST":
        form = MessageForm(request.POST, instance=msg)
        if form.is_valid():
            form.save()
            return redirect("dashboard_messages")
    else:
        form = MessageForm(instance=msg)
    return render(request, "dashboard/message_view.html", {"form": form, "message": msg})


@staff_member_required
def settings_view(request):
    settings = SiteSettings.load()
    if request.method == "POST":
        form = SiteSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect("dashboard_index")
    else:
        form = SiteSettingsForm(instance=settings)
    return render(request, "dashboard/settings.html", {"form": form})


@staff_member_required
def testimonials_mgmt(request):
    items = Testimonial.objects.order_by("-created")
    return render(request, "dashboard/testimonials_list.html", {"testimonials": items})


@staff_member_required
def testimonial_toggle(request, pk, action):
    t = get_object_or_404(Testimonial, pk=pk)
    if action == "approve":
        t.approved = True
    else:
        t.approved = False
    t.save()
    return redirect("dashboard_testimonials")


@staff_member_required
def services_mgmt(request):
    items = Service.objects.order_by("order")
    return render(request, "dashboard/services_list.html", {"services": items})
