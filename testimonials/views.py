from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Testimonial
from .forms import TestimonialSubmissionForm


def testimonials_list(request):
    qs = Testimonial.objects.filter(approved=True).order_by("-featured", "order")
    paginator = Paginator(qs, 6)
    page = request.GET.get("page")
    items = paginator.get_page(page)
    return render(request, "testimonials/testimonial_list.html", {"testimonials": items})


def testimonial_submit(request):
    if request.method == "POST":
        form = TestimonialSubmissionForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.approved = False
            t.save()
            return render(request, "testimonials/testimonial_submit_thanks.html", {"testimonial": t})
    else:
        form = TestimonialSubmissionForm()
    return render(request, "testimonials/testimonial_submit.html", {"form": form})
