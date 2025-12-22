from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("original-admin/", admin.site.urls),
    path("", include("core.urls")),
    path("portfolio/", include("portfolio.urls")),
    path("blog/", include("blog.urls")),
    path("contact/", include("contact.urls")),
    path("services/", include("services.urls")),
    path("about/", include("about_me.urls")),
    path("testimonials/", include("testimonials.urls")),
    path('admin/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
    path("favicon.ico", RedirectView.as_view(url="/static/favicon.ico", permanent=True)),
]
