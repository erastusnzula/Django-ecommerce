from django.db import models
from django.conf import settings

from src.models.product import Product


class CartProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    size = models.CharField(max_length=255, default="")

    def __str__(self):
        return f'{self.product.name} : {self.quantity}'

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_total_product_discount_price(self):
        return self.quantity * self.product.discount_price

    def get_amount_saved(self):
        return self.get_total_product_price() - self.get_total_product_discount_price()

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_product_discount_price()
        return self.get_total_product_price()
