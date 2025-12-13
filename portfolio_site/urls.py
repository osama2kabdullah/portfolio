from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("portfolio/", include("portfolio.urls")),
    path("blog/", include("blog.urls")),
    path("contact/", include("contact.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("favicon.ico", RedirectView.as_view(url="/static/favicon.ico", permanent=True)),
]
