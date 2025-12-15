from django.db import models


class SiteSettings(models.Model):
	site_title = models.CharField(max_length=200, default="My Portfolio")
	tagline = models.CharField(max_length=250, blank=True)
	logo = models.ImageField(upload_to="site/", blank=True, null=True)
	about = models.TextField(blank=True)
	contact_email = models.EmailField(blank=True)
	github = models.URLField(blank=True)
	twitter = models.URLField(blank=True)
	linkedin = models.URLField(blank=True)

	class Meta:
		verbose_name = "Site Settings"

	def __str__(self):
		return "Site Settings"

	def save(self, *args, **kwargs):
		self.pk = 1
		super().save(*args, **kwargs)

	@classmethod
	def load(cls):
		obj, created = cls.objects.get_or_create(pk=1)
		return obj
