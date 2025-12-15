from django.shortcuts import render, redirect
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


def thanks(request):
    if not request.session.get("form_submitted"):
        return redirect("contact")
    del request.session["form_submitted"]
    return render(request, "contact/thanks.html", {"show_footer_contact": False})
