from django.db import models
from services.models import Service

class Message(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    budget = models.DecimalField(
        max_digits=10,  # total digits
        decimal_places=2,  # digits after decimal
        null=True,
        blank=True,
        help_text="Estimated budget in USD"
    )
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"Message from {self.name}"

class ContactSettings(models.Model):
    sender_name = models.CharField(
        max_length=100,
        default="Osama Abdullah",
        help_text="Name displayed as the sender in emails"
    )
    recipient_email = models.EmailField(default="abdullah21673@hotmail.com")
    sender_email = models.EmailField(default="osama2kabdullah@gmail.com")

    def __str__(self):
        return f"Contact Settings: {self.sender_email} → {self.recipient_email}"

    class Meta:
        verbose_name = "Contact Settings"
        verbose_name_plural = "Contact Settings"