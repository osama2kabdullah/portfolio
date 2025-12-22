from django.contrib import admin
from .models import Client, Project, ProjectSection, Skill, ProjectImage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


class ProjectSectionInline(admin.TabularInline):
    model = ProjectSection
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "client", "year", "featured", "published", "created")
    list_filter = ("published", "featured", "services", "technologies", "year")
    search_fields = ("title", "excerpt", "client__name", "client__company_name")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("technologies", "services")
    inlines = (ProjectSectionInline, ProjectImageInline)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "company_name", "email", "whatsapp")
    search_fields = ("name", "company_name", "email")

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "order")
    ordering = ("-level",)


@admin.register(ProjectSection)
class ProjectSectionAdmin(admin.ModelAdmin):
    list_display = ("project", "heading", "order", "is_highlight")
    list_filter = ("is_highlight", "project")
    search_fields = ("heading", "subheading", "body", "project__title")
    ordering = ("order",)


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ("project", "caption", "order")
    list_filter = ("project",)
    search_fields = ("caption", "project__title")
    ordering = ("order",)
