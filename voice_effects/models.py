from django.db import models
import subprocess


class Effect(models.Model):
    template = models.JSONField()  # Store command as a list, e.g. ["echo", "{input}"]

    def process(self, input):
        # Replace placeholders safely in each argument
        command = [part.format(input=input) for part in self.template]
        result = subprocess.run(command, capture_output=True, text=True)
