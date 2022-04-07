from django.db import models
from django.conf import settings

from django_countries.fields import CountryField
from PIL import Image, ExifTags


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile", help_text="Add a profile photo", verbose_name='Profile Photo')
    phone_number = models.CharField(max_length=100, help_text='Enter a valid phone number')
    email = models.EmailField()
    country = CountryField(multiple=False, blank_label='(Select country)', help_text='Select your residence country')

    def __str__(self):
        return f'{self.country.name}'

    """
    def resize_image(self):
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save()
        self.resize_image()
    """
