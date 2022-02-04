from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.views import View

from src.models.product import Product, Category


def product_category(request, category):
    product_categories = Product.objects.filter(category__name__contains=category).order_by('-added_on')
    paginator = Paginator(product_categories, 4)
    page_number = request.GET.get('page')
    try:
        products = paginator.get_page(page_number)

    except EmptyPage:
        products = paginator.get_page(page_number)

    context = {
        'products': products,
        'category': category,
    }
    return render(request, 'src/category.html', context)


def all_categories(request):
    categories = Category.objects.all()
    return {'categories': categories}
