from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "service", "is_read", "created")
    list_filter = ("is_read",)
    readonly_fields = ("name", "email", "service", "budget", "body", "created")
    actions = ["mark_as_read"]

    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"Marked {updated} message(s) as read.")

    mark_as_read.short_description = "Mark selected messages as read"
