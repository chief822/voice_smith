from django import forms
from django.core.exceptions import ValidationError
import os

def validate_file_size(value):
    limit = 10 * 1024 * 1024  # 10 MB
    if value.size > limit:
        raise ValidationError("File too large. Size should not exceed 10 MB.")

class AudioInput(forms.Form):
    audio = forms.FileField(
        required=False,
        validators=[validate_file_size],
        help_text="Upload an audio file (max 10 MB)."
    )
