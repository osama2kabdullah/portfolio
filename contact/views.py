from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from portfolio_site.utils import render_thanks
from .forms import ContactForm
from .models import ContactSettings

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save()

            # Get ContactSettings singleton
            settings_obj = ContactSettings.objects.first()
            if settings_obj:
                sender_email = settings_obj.sender_email or settings.EMAIL_HOST_USER
                sender_name = settings_obj.sender_name or "Portfolio Contact"
                recipient_email = settings_obj.recipient_email or settings.EMAIL_HOST_USER
            else:
                sender_email = settings.EMAIL_HOST_USER
                sender_name = "Portfolio Contact"
                recipient_email = settings.EMAIL_HOST_USER

            # 1️⃣ Admin notification
            subject_admin = f"New Contact Message from Portfolio Website"
            context_admin = {"message": message}
            text_admin = render_to_string("emails/contact_notification.txt", context_admin)
            html_admin = render_to_string("emails/contact_notification.html", context_admin)

            email_admin = EmailMultiAlternatives(
                subject=subject_admin,
                body=text_admin,
                from_email=f"{sender_name} <{sender_email}>",
                to=[recipient_email],
                reply_to=[message.email],
            )
            email_admin.attach_alternative(html_admin, "text/html")
            email_admin.send(fail_silently=False)

            # 2️⃣ Auto-reply to user
            subject_user = "Thank you for contacting me!"
            context_user = {"message": message}

            text_user = render_to_string("emails/contact_autoreply.txt", context_user)
            html_user = render_to_string("emails/contact_autoreply.html", context_user)

            email_user = EmailMultiAlternatives(
                subject=subject_user,
                body=text_user,
                from_email=f"{sender_name} <{sender_email}>",
                to=[message.email],
            )
            email_user.attach_alternative(html_user, "text/html")
            email_user.send(fail_silently=False)

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
