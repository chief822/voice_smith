from django.db import models
import subprocess


class Effects(models.Model):
    template = models.JSONField()  # Store command as a list, e.g. ["echo", "{input}"]

    def command(self, input, output):
        # Replace placeholders safely in each argument
        return [part.format(input=input, output=output) for part in self.template]
