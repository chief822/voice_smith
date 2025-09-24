from django.db import models
import shlex
from django.core.exceptions import ValidationError

class Effects(models.Model):
    name = models.CharField(max_length=100, unique=True, default="New Effect")
    description = models.TextField(blank=True, default="")

    # be sure to give {input} and {output} placeholders
    template = models.JSONField()  # Store command as a list, e.g. ["echo", "{input}"]

    def clean(self):
        super().clean()

        # Ensure template is a list of strings
        if not isinstance(self.template, list) or not all(isinstance(x, str) for x in self.template):
            raise ValidationError({"template": "Template must be a list of strings."})

        # Flatten into one string for easier searching
        full_text = " ".join(self.template)

        # Check for placeholders
        if "{input}.wav" not in full_text:
            raise ValidationError({"template": "Template must include '{input}.wav'."})

        if "{output}.wav" not in full_text:
            raise ValidationError({"template": "Template must include '{output}.wav'."})

    def command(self, *, input, output):
        # Replace placeholders safely in each argument
        return [part.format(input=input, output=output) for part in self.template]
