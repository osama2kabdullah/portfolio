from django.contrib import admin
from .models import Profile, Journey, CoreValue, AboutSettings

class JourneyInline(admin.TabularInline):
    model = Journey
    extra = 1

class CoreValueInline(admin.TabularInline):
    model = CoreValue
    extra = 1

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "is_active")
    filter_horizontal = ("skills",)
    inlines = [JourneyInline, CoreValueInline]

@admin.register(AboutSettings)
class AboutSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # prevent creating multiple instances
        return not AboutSettings.objects.exists()