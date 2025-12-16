from django.shortcuts import render, redirect

from portfolio_site.utils import render_thanks
from .forms import ContactForm


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            request.session["form_submitted"] = True
            return redirect("contact_thanks")
    else:
        form = ContactForm()
    return render(request, "contact/contact.html", {"form": form, "show_footer_contact": False})


def contact_thanks(request):
    return render_thanks(
        request,
        session_key="form_submitted",
        redirect_url="contact",
        extra_context={
            "show_footer_contact": False,
            "title": "Thanks",
            "heading": "Thank You for Your Project Inquiry.",
            "subheading": "Submission Received",
            "message": "Your detailed message has been successfully sent. I am excited to review your vision and determine if we are a perfect fit. I will personally respond to your email within 1-2 business days.",
            "project": None,
        }
    )
