from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from src.models import Order


class TrackOrder(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.filter(user=self.request.user, ordered=True)
            context = {'object': order}
            return render(self.request, 'src/track_order.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, 'You have not placed any order.')
            return redirect('src:home')
