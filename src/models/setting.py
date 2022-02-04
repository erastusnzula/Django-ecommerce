from django.db import models

from ckeditor.fields import RichTextField


class Setting(models.Model):
    company_name = models.CharField(max_length=255,blank=True, null=True)
    company_location = models.CharField(max_length=255,blank=True, null=True)
    company_contact = models.CharField(max_length=255,blank=True, null=True)
    company_about = RichTextField(blank=True, null=True)
    company_motto = models.CharField(max_length=500,blank=True, null=True)

    def __str__(self):
        return 'EBM - Company Settings.'
