from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path("original-admin/", admin.site.urls),
    path("", include("core.urls")),
    path("projects/", include("projects.urls")),
    path("blog/", include("blog.urls")),
    path("contact/", include("contact.urls")),
    path("services/", include("services.urls")),
    path("about/", include("about_me.urls")),
    path("testimonials/", include("testimonials.urls")),
    path('admin/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
    path("bn/", include("bn.urls")),
]+ debug_toolbar_urls()
