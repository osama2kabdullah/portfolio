from django.shortcuts import render, redirect
from portfolio_site.utils import render_thanks
from .forms import ContactForm
from .services import handle_contact_submission

def contact_view(request):
    form_config = {
        "name": {
            "label": "Your Full Name*",
            "placeholder": "e.g. John Doe",
        },
        "email": {
            "label": "Work Email*",
            "placeholder": "name@company.com",
        },
        "service": {
            "label": "What service are you interested in?",
        },
        "budget": {
            "label": "Estimated Budget Range (BDT)*",
            "placeholder": "e.g. 50000",
        },
        "body": {
            "label": "Project Details / Goals*",
            "placeholder": "Tell me about your project...",
        },
    }

    if request.method == "POST":
        form = ContactForm(request.POST, config=form_config)
        if form.is_valid():
            handle_contact_submission(
                form=form,
                request=request,
                admin_subject="New Contact Message",
                admin_templates={
                    "text": "emails/contact_notification.txt",
                    "html": "emails/contact_notification.html",
                },
                user_subject="Thank you for contacting me!",
                user_templates={
                    "text": "emails/contact_autoreply.txt",
                    "html": "emails/contact_autoreply.html",
                },
            )
            return redirect("contact_thanks")
    else:
        form = ContactForm(config=form_config)

    return render(request, "contact/contact.html", {"form": form})

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
