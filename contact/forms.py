from django import forms
from services.models import Service
from .models import Message


class ContactForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(published=True),
        empty_label="-- Select Service --",
        required=False
    )

    class Meta:
        model = Message
        fields = ["name", "email", "service", "budget", "body"]

    def __init__(self, *args, **kwargs):
        config = kwargs.pop("config", {})
        super().__init__(*args, **kwargs)

        for field_name, field_config in config.items():
            if field_name not in self.fields:
                continue

            field = self.fields[field_name]

            if "label" in field_config:
                field.label = field_config["label"]

            if "help_text" in field_config:
                field.help_text = field_config["help_text"]

            if "placeholder" in field_config:
                field.widget.attrs["placeholder"] = field_config["placeholder"]

        # Remove fields if needed
        remove_fields = config.get("_remove", [])
        for field_name in remove_fields:
            self.fields.pop(field_name, None)
