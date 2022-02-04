# Generated by Django 4.0 on 2021-12-18 10:35

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0017_alter_article_slug_alter_product_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('body', ckeditor.fields.RichTextField()),
                ('date_commented', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=ckeditor.fields.RichTextField(default='I can marry Erastus anytime anywhere.'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(default='Test Product - 11 ', max_length=100),
        ),
    ]