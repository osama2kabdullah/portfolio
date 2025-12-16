from django.shortcuts import render, redirect

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
