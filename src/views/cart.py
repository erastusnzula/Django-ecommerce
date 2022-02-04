from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from src.models import Product, CartProduct, Order


@login_required
def add_to_cart(request, slug):
    """Adjust an item's quantity positively (cart summary option + )."""
    product = get_object_or_404(Product, slug=slug)
    order_product, created = CartProduct.objects.get_or_create(product=product, user=request.user, ordered=False)
    qs = Order.objects.filter(user=request.user, ordered=False)
    if qs.exists():
        order = qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(request, f'{order_product.product.name.title()} quantity updated successfully.')
            return redirect('src:cart-summary')
        else:
            order.products.add(order_product)
            messages.info(request, f'{order_product.product.name.title()} added to cart successfully.')
            return redirect('src:cart-summary')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.products.add(order_product)
        messages.info(request, f'{order_product.product.name.title()} added to cart successfully.')
        return redirect('src:cart-summary')


def adjust_cart_quantity_home(request, slug):
    """Adjust an item's quantity positively (cart summary option + )."""
    product = get_object_or_404(Product, slug=slug)
    order_product, created = CartProduct.objects.get_or_create(product=product, user=request.user, ordered=False)
    qs = Order.objects.filter(user=request.user, ordered=False)
    if qs.exists():
        order = qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(request, f'{order_product.product.name.title()} quantity updated successfully.')
            return redirect('src:home')
        else:
            order.products.add(order_product)
            messages.info(request, f'{order_product.product.name.title()} added to cart successfully.')
            return redirect('src:home')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.products.add(order_product)
        messages.info(request, f'{order_product.product.name.title()} added to cart successfully.')
        return redirect('src:home')


@login_required
def add_to_cart_home(request, slug):
    """Add an item to cart (Homepage)."""
    product = get_object_or_404(Product, slug=slug)
    order_product, created = CartProduct.objects.get_or_create(product=product, user=request.user, ordered=False)
    qs = Order.objects.filter(user=request.user, ordered=False)
    if qs.exists():
        order = qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(request,
                          f'{order_product.quantity} {order_product.product.name.title()}s added to cart successfully.')

            return redirect('src:home')
        else:
            order.products.add(order_product)
            messages.info(request, f'{order_product.product.name.title()} added to cart successfully.')
            return redirect('src:home')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.products.add(order_product)
        messages.info(request, f'{order_product.product.name.title()} added to cart successfully.')
        return redirect('src:home')


@login_required
def add_to_cart_product(request, slug):
    """Add an item to cart (Product detail view)."""
    product = get_object_or_404(Product, slug=slug)
    order_product, created = CartProduct.objects.get_or_create(product=product, user=request.user, ordered=False)
    qs = Order.objects.filter(user=request.user, ordered=False)
    if qs.exists():
        order = qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(request,
                          f'{order_product.quantity} {order_product.product.name.title()}s added to cart successfully.')
            return redirect('src:product', slug=slug)
        else:
            order.products.add(order_product)
            messages.info(request, f'{order_product.product.name.title()} added to cart successfully.')
            return redirect('src:product', slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.products.add(order_product)
        messages.info(request, f'{order_product.product.name.title()} added to cart successfully.')
        return redirect('src:product', slug=slug)


@login_required
def remove_from_cart(request, slug):
    """Remove an item from cart (cart summary view)."""
    product = get_object_or_404(Product, slug=slug)
    qs = Order.objects.filter(user=request.user, ordered=False)
    if qs.exists():
        order = qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product = CartProduct.objects.filter(product=product, user=request.user, ordered=False)[0]
            order.products.remove(order_product)
            messages.info(request, f'{order_product.product.name.title()} removed from cart successfully.')
            return redirect('src:cart-summary')
        else:
            messages.warning(request, f'{request.user.username.title()}, this product is not in your cart!')
            return redirect('src:product', slug=slug)
    else:
        messages.warning(request,
                         f'{request.user.username.title()}, you do not have an active order, consider placing one.')
        return redirect('src:product', slug=slug)


@login_required
def remove_from_cart_product(request, slug):
    """"Remove an item from cart (Product details view)."""
    product = get_object_or_404(Product, slug=slug)
    qs = Order.objects.filter(user=request.user, ordered=False)
    if qs.exists():
        order = qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product = CartProduct.objects.filter(product=product, user=request.user, ordered=False)[0]
            order.products.remove(order_product)
            messages.info(request, f'{order_product.product.name.title()} removed from cart successfully.')
            return redirect('src:product', slug=slug)
        else:
            messages.warning(request, f'{request.user.username.title()}, this product is not in your cart!')
            return redirect('src:product', slug=slug)
    else:
        messages.warning(request,
                         f'{request.user.username.title()}, you do not have an active order, consider placing one.')
        return redirect('src:product', slug=slug)

@login_required
def remove_product_home(request, slug):
    """Adjust cart product negatively quantity (-)"""
    product = get_object_or_404(Product, slug=slug)
    qs = Order.objects.filter(user=request.user, ordered=False)
    if qs.exists():
        order = qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product = CartProduct.objects.filter(product=product, user=request.user, ordered=False)[0]
            if order_product.quantity > 1:
                order_product.quantity -= 1
                order_product.save()

            else:
                order.products.remove(order_product)
            messages.info(request, f'{order_product.product.name.title()} quantity updated successfully.')
            return redirect('src:home')
        else:
            messages.warning(request, f'{request.user.username.title()}, this product not in your cart!')
            return redirect('src:home')
    else:
        messages.warning(request,
                         f'{request.user.username.title()}, you do not have an active order consider placing one.')
        return redirect('src:product', slug=slug)



@login_required
def remove_single_product_from_cart(request, slug):
    """Adjust cart product negatively quantity (-)"""
    product = get_object_or_404(Product, slug=slug)
    qs = Order.objects.filter(user=request.user, ordered=False)
    if qs.exists():
        order = qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product = CartProduct.objects.filter(product=product, user=request.user, ordered=False)[0]
            if order_product.quantity > 1:
                order_product.quantity -= 1
                order_product.save()

            else:
                order.products.remove(order_product)
            messages.info(request, f'{order_product.product.name.title()} quantity updated successfully.')
            return redirect('src:cart-summary')
        else:
            messages.warning(request, f'{request.user.username.title()}, this product not in your cart!')
            return redirect('src:product', slug=slug)
    else:
        messages.warning(request,
                         f'{request.user.username.title()}, you do not have an active order consider placing one.')
        return redirect('src:product', slug=slug)
