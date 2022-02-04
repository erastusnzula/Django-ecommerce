# Generated by Django 4.0 on 2021-12-13 09:38

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0007_alter_product_description_alter_product_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(default='Clothes', max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(related_name='products', to='src.Category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=ckeditor.fields.RichTextField(default='I love this product so much.'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(default='Test Product - 78 ', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='seller',
            field=models.CharField(choices=[('N', 'EMU'), ('F', 'ETBM'), ('P', 'ETBM')], default='EMU', max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(related_name='sizes', to='src.Size'),
        ),
    ]