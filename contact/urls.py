from django.urls import path
from . import views

urlpatterns = [
    path("", views.contact_view, name="contact"),
    path("thanks/", views.thanks, name="contact_thanks"),
]
