from django import forms
from .models import Testimonial
from projects.models import Client, Project


class TestimonialSubmissionForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["name", "email", "company", "role", "body", "project"]
        widgets = {
            "body": forms.Textarea(attrs={
                "rows": 6,
                "placeholder": "Share your experience working with me…"
            }),
        }

    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)

        # If project is forced via URL → hide selector
        if project:
            self.fields["project"].widget = forms.HiddenInput()
            self.initial["project"] = project
        else:
            self.fields["project"].queryset = Project.objects.filter(published=True)
            self.fields["project"].required = False

    def save(self, commit=True):
        testimonial = super().save(commit=False)

        email = self.cleaned_data.get("email")

        if email:
            client, _ = Client.objects.get_or_create(
                email=email,
                defaults={
                    "name": self.cleaned_data["name"],
                    "company_name": self.cleaned_data.get("company", ""),
                },
            )
            testimonial.client = client

        if commit:
            testimonial.save()

        return testimonial
