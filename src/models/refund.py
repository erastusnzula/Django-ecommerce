from django.db import models
from django.conf import settings

from src.models.order import Order


class Refund(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField(help_text="Enter a valid reason for requesting a refund.",
                              verbose_name="Reason for requesting a refund")
    ref_code = models.CharField(max_length=200, verbose_name="Reference code",
                                help_text="Enter a valid reference code.")
    accepted = models.BooleanField(default=False)
    email = models.EmailField()
    date_req = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reason[:20]}..."
