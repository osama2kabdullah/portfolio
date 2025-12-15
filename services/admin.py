from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "published", "order")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "description")
    ordering = ("order",)
from django.contrib import admin

# Register your models here.
