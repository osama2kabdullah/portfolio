from django.contrib import admin
from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "role", "approved", "featured", "order")
    list_filter = ("approved", "featured")
    ordering = ("-featured", "order")
    actions = ["approve_testimonials", "decline_testimonials"]

    def approve_testimonials(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, f"Approved {updated} testimonial(s)")

    def decline_testimonials(self, request, queryset):
        updated = queryset.update(approved=False)
        self.message_user(request, f"Declined {updated} testimonial(s)")

    approve_testimonials.short_description = "Approve selected testimonials"
    decline_testimonials.short_description = "Decline selected testimonials"
from django.contrib import admin

# Register your models here.
