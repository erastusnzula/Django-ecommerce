from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from src.models.article import Article, Comment
from src.forms import CommentForm


class Articles(ListView):
    model = Article
    paginate_by = 5
    ordering = ['-date_added']
    template_name = 'src/articles.html'


class ArticleDetails(View):
    def get(self, request, slug):
        article = Article.objects.get(slug=slug)
        comments = Comment.objects.filter(article=article)
        form = CommentForm()
        context = {
            'form': form,
            'article': article,
            'comments': comments,
        }
        return render(request, 'src/article_details.html', context)

    def post(self, request, slug):
        article = Article.objects.get(slug=slug)
        form = CommentForm(self.request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            body = form.cleaned_data.get('body')
            comment = Comment()
            comment.name = name
            comment.email = email
            comment.body = body
            comment.article = article
            comment.save()
            messages.success(request, "Comment send successfully.")
            return redirect('src:article-details', slug=slug)


def article_category(request, category):
    article_categories = Article.objects.filter(category__name__contains=category).order_by('-date_added')
    paginator = Paginator(article_categories, 5)
    page_number = request.GET.get('page')
    try:
        articles = paginator.get_page(page_number)

    except EmptyPage:
        articles = paginator.get_page(page_number)

    context = {
        'articles': articles,
        'category': category,
    }
    return render(request, 'src/article_category.html', context)
