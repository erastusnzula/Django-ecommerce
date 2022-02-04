from django.views.generic import ListView

from src.models import Product


class HomeView(ListView):
    model = Product
    paginate_by = 4
    ordering = ['-added_on']
    template_name = 'src/home.html'
