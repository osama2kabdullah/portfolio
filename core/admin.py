from django.contrib import admin
from .models import SiteSettings

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):

    fieldsets = (
        ("Site Info / Favicon", {
            "fields": ("site_title", "tagline", "logo", "favicon")
        }),
        ("Footer / About", {
            "fields": ("about_short", "footer_text")
        }),
        ("SEO / Social Preview", {
            "fields": (
                "meta_title",
                "meta_description",
                "og_title",
                "og_description",
                "og_image",
                "twitter_card"
            )
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True
