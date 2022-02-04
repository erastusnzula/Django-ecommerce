from django.views import View
from django.shortcuts import render, redirect

from src.models import Product


class SearchProduct(View):
    def post(self, request):
        query_name = request.POST.get('name')
        if query_name:
            products = Product.objects.filter(name__contains=query_name)
            return render(request, 'src/search.html', {'products': products, 'query_name': query_name})
        else:
            return redirect('src:home')
