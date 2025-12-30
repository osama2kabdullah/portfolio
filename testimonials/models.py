from django.db import models
from projects.models import Client, Project
from django.utils import timezone

class Testimonial(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name="testimonials")
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name="testimonials")
    
    name = models.CharField(max_length=140)
    role = models.CharField(max_length=140, blank=True)
    company = models.CharField(max_length=140, blank=True)
    body = models.TextField()
    email = models.EmailField(blank=True)

    rating = models.PositiveSmallIntegerField(
        default=5,
        choices=[(i, f"{i} Stars") for i in range(1, 6)],
        help_text="Rating out of 5",
    )
    
    featured = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-featured", "order"]

    def __str__(self):
        return f"{self.name} — {self.company or ''}"

class TestimonialPageSettings(models.Model):
    """
    Singleton model to store dynamic text for testimonial pages.
    """
    # Submission page
    submit_heading = models.CharField(max_length=200, default="Leave a Testimonial for AlexDev")
    submit_subheading = models.TextField(default="Your honest feedback is invaluable. Thank you for being a fantastic client!")
    
    # Thank you page
    thanks_title = models.CharField(max_length=200, default="Thank You for Your Testimonial")
    thanks_subheading = models.CharField(max_length=200, default="Testimonial Received")
    thanks_message = models.TextField(default="Your testimonial has been received and will appear on the site after approval.")
    
    def __str__(self):
        return "Testimonial Page Settings"

    class Meta:
        verbose_name = "Testimonial Page Settings"
        verbose_name_plural = "Testimonial Page Settings"
