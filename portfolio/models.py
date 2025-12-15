from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=100)
    level = models.PositiveSmallIntegerField(default=1, help_text="1-100")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["-level", "order"]

    def __str__(self):
        return f"{self.name} ({self.level})"

class Client(models.Model):
    name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    whatsapp = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name="projects")
    excerpt = models.TextField(blank=True)
    hero_description = models.TextField(blank=True)
    live_url = models.URLField(blank=True)
    repo_url = models.URLField(blank=True)
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    
    technologies = models.ManyToManyField("Skill", blank=True, related_name="projects")
    services = models.ManyToManyField("services.Service", blank=True, related_name="projects")

    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    timeline = models.CharField(max_length=100, blank=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-featured", "-created"]

    def __str__(self):
        return self.title

class ProjectSection(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="sections"
    )
    heading = models.CharField(max_length=200)
    subheading = models.CharField(max_length=300, blank=True)
    body = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)
    is_highlight = models.BooleanField(
        default=False,
        help_text="Use for testimonials, results, or special callouts"
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.project.title} — {self.heading}"

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="projects/images/")
    caption = models.CharField(max_length=220, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.project.title} image ({self.id})"
