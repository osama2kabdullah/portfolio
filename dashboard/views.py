from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings


def staff_required(user):
    return user.is_staff

# Login view
def login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard:dashboard_index')

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                return redirect('dashboard:dashboard_index')
            else:
                messages.error(request, "You do not have staff access.")
        else:
            # Form invalid -> shows errors automatically
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
            for error in form.non_field_errors():
                messages.error(request, error)

    return render(request, 'dashboard/login.html', {'form': form})

# Logout
@login_required
def logout_view(request):
    logout(request)
    return redirect('dashboard:login')

# Dashboard
@login_required
@user_passes_test(staff_required)
def dashboard_index(request):
    return render(request, 'dashboard/index.html')
