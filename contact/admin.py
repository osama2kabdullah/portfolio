from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_read", "created")
    list_filter = ("is_read",)
    readonly_fields = ("name", "email", "subject", "body", "created")
