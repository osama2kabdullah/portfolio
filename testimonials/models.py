from django.db import models


class Testimonial(models.Model):
    name = models.CharField(max_length=140)
    role = models.CharField(max_length=140, blank=True)
    company = models.CharField(max_length=140, blank=True)
    body = models.TextField()
    email = models.EmailField(blank=True)
    project = models.ForeignKey("portfolio.Project", on_delete=models.SET_NULL, null=True, blank=True, related_name="testimonials")
    featured = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["-featured", "order"]

    def __str__(self):
        return f"{self.name} — {self.company or ''}"
from django.db import models

# Create your models here.
