# Generated by Django 4.0 on 2021-12-13 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0009_alter_category_name_alter_product_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='thumbnail',
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(default='Test Product - 13 ', max_length=100),
        ),
    ]