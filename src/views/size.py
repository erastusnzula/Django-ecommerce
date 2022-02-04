from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from src.models.cartproducts import CartProduct
from src.models.product import Product


def product_size(request, size):
    product_sizes = Product.objects.filter(size__name__contains=size).order_by('-added_on')
    paginator = Paginator(product_sizes, 4)
    page_number = request.GET.get('page')
    try:
        products = paginator.get_page(page_number)

    except EmptyPage:
        products = paginator.get_page(page_number)

    context = {
        'products': products,
        'size': size,
    }
    return render(request, 'src/size.html', context)


class SelectSize(LoginRequiredMixin, View):
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        size = request.POST.getlist('size')
        if size:
            order_product, created = CartProduct.objects.get_or_create(product=product, user=request.user,
                                                                       ordered=False)
            order_product.size = ','.join(size)

            order_product.save()
            messages.success(self.request,
                             f"Size: {','.join(size)} saved successfully, now please add the item to cart")
            return redirect('src:product', slug=slug)
        else:
            return redirect('src:product', slug=slug)

    def get(self, request, slug):
        messages.success(self.request, "Now select size and add the item to cart.")
        return redirect('src:product', slug=slug)
