from django.shortcuts import render, redirect
import resend
from django.conf import settings
from threading import Thread
import logging

logger = logging.getLogger(__name__)

resend.api_key = settings.RESEND_API_KEY

def render_thanks(request, session_key, redirect_url, template="general/thanks.html", extra_context=None):
    """
    Shared logic for thank-you pages:
    - Checks session key
    - Deletes session flag
    - Renders the template with extra context
    """
    if not request.session.get(session_key):
        return redirect(redirect_url)

    del request.session[session_key]

    context = extra_context or {}
    return render(request, template, context)

def send_resend_email(
    *,
    subject: str,
    to: list[str],
    html: str,
    text: str | None = None,
    reply_to: str | None = None,
    sender_name="Portfolio Website",
):
    payload = {
        "from": f"{sender_name} <{settings.RESEND_FROM_EMAIL}>",
        "to": to,
        "subject": subject,
        "html": html,
    }

    if text:
        payload["text"] = text

    if reply_to:
        payload["reply_to"] = reply_to

    return resend.Emails.send(payload)


def send_resend_email_async(**kwargs):
    def _send():
        try:
            send_resend_email(**kwargs)
        except Exception:
            logger.exception("Resend email failed")

    Thread(target=_send, daemon=True).start()
