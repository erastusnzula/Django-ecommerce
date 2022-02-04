from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from src.models import Order


class CartSummary(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        """Display cart items."""
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {'object': order}
            return render(self.request, 'src/cart_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, 'You do not have an active order.')
            return redirect('/')
