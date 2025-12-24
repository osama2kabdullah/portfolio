from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from portfolio_site.utils import render_thanks
from .forms import ContactForm
from .models import ContactSettings
from portfolio_site.utils import send_resend_email_async

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save()

            settings_obj = ContactSettings.objects.first()
            sender_name = settings_obj.sender_name or "Portfolio Website"
            recipient_email = (
                settings_obj.recipient_email
                if settings_obj and settings_obj.recipient_email
                else settings.RESEND_FROM_EMAIL
            )

            # Get ContactSettings singleton
            subject_admin = "New Contact Message from Portfolio Website"
            context_admin = {"message": message}

            text_admin = render_to_string(
                "emails/contact_notification.txt", context_admin
            )
            html_admin = render_to_string(
                "emails/contact_notification.html", context_admin
            )

            send_resend_email_async(
                subject=subject_admin,
                to=[recipient_email],
                text=text_admin,
                html=html_admin,
                reply_to=message.email,
                sender_name=sender_name,
            )

            # 2️⃣ Auto-reply to user
            subject_user = "Thank you for contacting me!"
            context_user = {"message": message}

            text_user = render_to_string(
                "emails/contact_autoreply.txt", context_user
            )
            html_user = render_to_string(
                "emails/contact_autoreply.html", context_user
            )

            send_resend_email_async(
                subject=subject_user,
                to=[message.email],
                text=text_user,
                html=html_user,
                sender_name=sender_name,
            )

            request.session["form_submitted"] = True
            return redirect("contact_thanks")
    else:
        form = ContactForm()

    return render(
        request,
        "contact/contact.html",
        {"form": form, "show_footer_contact": False},
    )

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
