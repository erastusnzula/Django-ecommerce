from src.models import Product
from django.views.generic import DetailView


class ProductDetail(DetailView):
    model = Product
    template_name = 'src/product.html'

