from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=100)
    level = models.PositiveSmallIntegerField(default=1, help_text="1-100")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["-level", "order"]

    def __str__(self):
        return f"{self.name} ({self.level})"


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField()
    excerpt = models.TextField(blank=True)
    url = models.URLField(blank=True)
    repo_url = models.URLField(blank=True)
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    technologies = models.ManyToManyField("Skill", blank=True, related_name="projects")
    services = models.ManyToManyField("services.Service", blank=True, related_name="projects")
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-featured", "-created"]

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="projects/images/")
    caption = models.CharField(max_length=220, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.project.title} image ({self.id})"
