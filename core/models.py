from django.db import models
from django.core.exceptions import ValidationError

class SiteSettings(models.Model):
    # Site Info
    site_title = models.CharField(max_length=200, default="My Portfolio")
    tagline = models.CharField(max_length=250, blank=True)
    logo = models.ImageField(upload_to="site/", blank=True, null=True)
    favicon = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True,
        help_text="Upload favicon (16x16 or 32x32, max 100KB)"
    )

    def clean(self):
        super().clean()
        if self.favicon and self.favicon.size > 102400:
            raise ValidationError({
                "favicon": "Favicon file size must be under 100KB."
            })

    # Footer / About
    about_short = models.TextField(blank=True)
    footer_text = models.TextField(blank=True)

    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    og_title = models.CharField(max_length=200, blank=True)
    og_description = models.CharField(max_length=160, blank=True)
    og_image = models.ImageField(upload_to="site/seo/", blank=True, null=True)
    twitter_card = models.CharField(max_length=50, default="summary_large_image", blank=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
