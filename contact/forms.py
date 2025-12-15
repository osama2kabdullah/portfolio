from django import forms
from services.models import Service
from .models import Message


class ContactForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(published=True),
        empty_label="-- Select Service --",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Message
        fields = ["name", "email", "service", "budget", "body"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "budget": forms.Select(attrs={"class": "form-control"}),
            "budget": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "placeholder": "USD"}),
            "body": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 6,
                "placeholder": "Tell me about your brand, what you need built..."
            }),
        }
