from django.db import models
from django.conf import settings

from django_countries.fields import CountryField

ADDRESS_CHOICES = (
    ('B', 'Billing Address'),
    ('S', 'Shipping Address'),
)


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    town = models.CharField(max_length=200)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=200)
    address_type = models.CharField(max_length=20, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'
