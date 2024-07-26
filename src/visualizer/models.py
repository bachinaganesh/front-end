from django.db import models
from django.utils import timezone

class File(models.Model):
    file = models.FileField()
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
