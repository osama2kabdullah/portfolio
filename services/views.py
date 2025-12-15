from django.shortcuts import render, get_object_or_404
from .models import Service
from django.core.paginator import Paginator


def service_detail(request, slug):
    svc = get_object_or_404(Service, slug=slug, published=True)
    return render(request, "services/service_detail.html", {"service": svc})

def service_list(request):
    qs = Service.objects.filter(published=True).order_by("-published")
    paginator = Paginator(qs, 6)
    page = request.GET.get("page")
    services = paginator.get_page(page)
    return render(request, "services/services_list.html", {"services": services})