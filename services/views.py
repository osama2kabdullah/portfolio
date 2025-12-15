from django.shortcuts import redirect, render, get_object_or_404
from .forms import ServiceContactForm
from .models import Service
from django.core.paginator import Paginator


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, published=True)

    if request.method == "POST":
        form = ServiceContactForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.service = service
            message.save()
            return redirect("contact_thanks")
    else:
        form = ServiceContactForm(initial={"service": service})

    return render(request, "services/service_detail.html", {
        "service": service,
        "form": form,
        "show_footer_contact": False
    })

def service_list(request):
    qs = Service.objects.filter(published=True).order_by("-published")
    paginator = Paginator(qs, 6)
    page = request.GET.get("page")
    services = paginator.get_page(page)
    return render(request, "services/services_list.html", {"services": services})