from django.db import models
from portfolio.models import Client, Project
from django.utils import timezone

class Testimonial(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name="testimonials")
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name="testimonials")
    
    name = models.CharField(max_length=140)
    role = models.CharField(max_length=140, blank=True)
    company = models.CharField(max_length=140, blank=True)
    body = models.TextField()
    email = models.EmailField(blank=True)
    
    featured = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-featured", "order"]

    def __str__(self):
        return f"{self.name} — {self.company or ''}"
