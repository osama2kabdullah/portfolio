from django.urls import path
from . import views

urlpatterns = [
    path("", views.contact_view, name="contact"),
    path("thanks/", views.contact_thanks, name="contact_thanks"),
]
