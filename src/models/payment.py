from django.db import models
from django.conf import settings


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=100, null=True, blank=True)
    paypal_order_key = models.CharField(max_length=1000, blank=True, null=True)
    paypal_user_id = models.CharField(max_length=1000, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    paypal_full_name = models.CharField(max_length=1000, blank=True, null=True)
    paypal_email = models.CharField(max_length=1000, blank=True, null=True)
    paypal_address1 = models.CharField(max_length=1000, blank=True, null=True)
    paypal_address2 = models.CharField(max_length=1000, blank=True, null=True)
    paypal_postal_code = models.CharField(max_length=1000, blank=True, null=True)
    paypal_country_code = models.CharField(max_length=1000, blank=True, null=True)
    amount = models.IntegerField()
    paypal_amount = models.CharField(max_length=1000, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
