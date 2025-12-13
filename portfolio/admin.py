from django.contrib import admin
from .models import Project, Skill


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "published", "featured", "created")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "description")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "order")
    ordering = ("-level",)
