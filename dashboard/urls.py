from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="dashboard_index"),
    path("projects/", views.projects_list, name="dashboard_projects"),
    path("projects/new/", views.project_create, name="dashboard_project_create"),
    path("projects/<int:pk>/edit/", views.project_edit, name="dashboard_project_edit"),
    path("posts/", views.posts_list, name="dashboard_posts"),
    path("messages/", views.messages_list, name="dashboard_messages"),
    path("messages/<int:pk>/", views.message_view, name="dashboard_message_view"),
    path("settings/", views.settings_view, name="dashboard_settings"),
    path("testimonials/", views.testimonials_mgmt, name="dashboard_testimonials"),
    path("testimonials/<int:pk>/<str:action>/", views.testimonial_toggle, name="dashboard_testimonial_toggle"),
    path("services/", views.services_mgmt, name="dashboard_services"),
]
