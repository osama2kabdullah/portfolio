from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from portfolio.models import Project, Skill
from blog.models import Post
from contact.models import Message


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
