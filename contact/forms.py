from django import forms
from .models import Message


class ContactForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["name", "email", "subject", "body"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 6}),
        }
