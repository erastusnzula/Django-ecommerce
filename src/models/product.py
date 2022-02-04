import itertools
import random

from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from ckeditor.fields import RichTextField
from PIL import Image

Description = [
    "I love this product so much.",
    "I can marry Erastus anytime anywhere.",
    "Wow! I have never seen anything like this before."
]

LABELS = (
    ('p', 'primary'),
    ('s', 'secondary'),
    ('d', 'danger'),
    ('i', 'info'),
    ('w', 'warning'),
    ('s', 'success'),
)

SELLER = (
    ('N', 'EMU'),
    ('F', 'ETBM'),
    ('P', 'ETBM'),
)


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, default=f"Test Product - {random.randint(1, 100)} ")
    category = models.ManyToManyField(Category, related_name='products')
    image = models.ImageField(upload_to='products')
    # thumbnail = models.ImageField(upload_to='products', null=True, blank=True)
    size = models.ManyToManyField(Size, related_name='sizes', blank=True)
    price = models.IntegerField(default=1500)
    discount_price = models.IntegerField(default=1000)
    slug = models.SlugField(unique=True, editable=False, blank=True, default="", max_length=5)
    label = models.CharField(max_length=100, choices=LABELS, default="primary")
    seller = models.CharField(max_length=200, choices=SELLER, default="EMU")
    description = RichTextField(default=f"{random.choice(Description)}")
    added_on = models.DateTimeField(auto_now_add=True)
    in_stock = models.BooleanField(default=True)
    stock_available = models.IntegerField(default=10)

    def __str__(self):
        return self.name

    def _generate_slug(self):
        max_length = self._meta.get_field('slug').max_length
        value = self.name[:max_length]
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Product.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, (i + 1))

        self.slug = slug_candidate

    """
    def resize_images(self):
        img = Image.open(self.thumbnail.path)
        if img.height > 300 or img.width > 300:
            size = (300, 300)
            img.thumbnail(size)
            img.save(self.thumbnail.path)
            """

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()

        super().save(*args, **kwargs)
        # self.resize_images()

    def get_absolute_url(self):
        return reverse('src:product', kwargs={'slug': self.slug})

    def add_to_cart_url(self):
        return reverse('src:add-to-cart', kwargs={'slug': self.slug})

    def add_to_cart_home_url(self):
        return reverse('src:add-to-cart-home', kwargs={'slug': self.slug})

    def add_to_cart_product_url(self):
        return reverse('src:add-to-cart-product', kwargs={'slug': self.slug})

    def remove_from_cart_url(self):
        return reverse('src:remove-from-cart', kwargs={'slug': self.slug})

    def remove_from_cart_product_url(self):
        return reverse('src:remove-from-cart-product', kwargs={'slug': self.slug})

    def remove_product_home_url(self):
        return reverse('src:remove-product-home', kwargs={'slug': self.slug})

    def adjust_cart_product_home_url(self):
        return reverse('src:adjust-cart-product-home', kwargs={'slug': self.slug})

    def get_product_images_url(self):
        product = Product.objects.get(slug=self.slug)
        return ProductImages.objects.filter(product=product)


class ProductImages(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products', blank=True)

    """
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
            """
