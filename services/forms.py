from contact.forms import ContactForm
from django import forms

class ServiceContactForm(ContactForm):
    def __init__(self, *args, **kwargs):
        service = kwargs.pop("service", None)
        super().__init__(*args, **kwargs)
        if service:
            self.fields["service"].initial = service
        self.fields["service"].widget = forms.HiddenInput()
