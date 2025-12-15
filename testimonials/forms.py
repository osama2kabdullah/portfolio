from django import forms
from .models import Testimonial


class TestimonialSubmissionForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["name", "email", "company", "role", "body", "project"]
        widgets = {"body": forms.Textarea(attrs={"rows": 4})}
