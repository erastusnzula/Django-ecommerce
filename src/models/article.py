import itertools

from django.conf import settings
from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils.text import slugify


class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Article categories"

    def __str__(self):
        return self.name


class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, editable=False, blank=True, default="", max_length=5)
    category = models.ManyToManyField(ArticleCategory, related_name='articles')
    description = RichTextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    def _generate_slug(self):
        max_length = self._meta.get_field('slug').max_length
        value = self.title[:max_length]
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Article.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, (i + 1))

        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()

        super().save(*args, **kwargs)

    def get_all_articles_url(self):
        return reverse('src:article-details', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    body = models.TextField(verbose_name='Enter comment')
    date_commented = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_commented']

    def __str__(self):
        return f'{self.name} : {self.article}'
