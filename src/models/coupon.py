from django.db import models


class Coupon(models.Model):
    code = models.CharField(max_length=50)
    amount = models.IntegerField()

    def __str__(self):
        return self.code
