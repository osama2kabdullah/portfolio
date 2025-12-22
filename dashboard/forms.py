from django import forms
from portfolio.models import Project, Skill
from blog.models import Post
from contact.models import Message
from core.models import SiteSettings
from django.contrib.auth.forms import SetPasswordForm

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': '••••••••',
            'id': 'new_password1'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': '••••••••',
            'id': 'new_password2'
        })


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "slug", "excerpt", "live_url", "repo_url", "published", "featured", "technologies"]
        widgets = {"technologies": forms.CheckboxSelectMultiple}


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "slug", "excerpt", "content", "published", "categories", "tags"]
        widgets = {"categories": forms.CheckboxSelectMultiple, "tags": forms.CheckboxSelectMultiple}


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "level", "order"]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["name", "email", "service", "budget", "body", "is_read"]


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ["site_title", "tagline", "about", "contact_email", "github", "twitter", "linkedin"]
