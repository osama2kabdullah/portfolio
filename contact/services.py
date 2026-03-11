from django.conf import settings
from django.template.loader import render_to_string
from portfolio_site.utils import send_django_email_async
from about_me.models import Profile
from contact.models import ContactSettings


def handle_contact_submission(
    *,
    form,
    request,
    admin_subject,
    admin_templates,
    user_subject,
    user_templates,
):
    message = form.save()

    # Prefer the singleton Profile contact info. Fall back to ContactSettings, then to settings.
    profile = Profile.load()
    sender_name = profile.full_name if profile and profile.full_name else "Portfolio Website"
    recipient_email = profile.email if profile and profile.email else None

    if not recipient_email:
        settings_obj = ContactSettings.objects.first()
        recipient_email = (
            getattr(settings_obj, "recipient_email", None)
            or settings.DEFAULT_FROM_EMAIL
        )

    # Admin email
    text_admin = render_to_string(
        admin_templates["text"], {"message": message}
    )
    html_admin = render_to_string(
        admin_templates["html"], {"message": message}
    )

    send_django_email_async(
        subject=admin_subject,
        to=[recipient_email],
        text=text_admin,
        html=html_admin,
        reply_to=message.email,
        sender_name=sender_name,
    )

    # User auto-reply
    text_user = render_to_string(
        user_templates["text"], {"message": message}
    )
    html_user = render_to_string(
        user_templates["html"], {"message": message}
    )

    send_django_email_async(
        subject=user_subject,
        to=[message.email],
        text=text_user,
        html=html_user,
        sender_name=sender_name,
    )

    request.session["form_submitted"] = True
