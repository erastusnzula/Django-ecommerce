from django.db import models
from django.conf import settings


class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField()
    message = models.TextField(help_text="You can message me about anything except the word fuck.")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:50]