from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages

from src.models.order import Order


class MpesaPayment(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {'order': order, 'DISPLAY_COUPON_FORM': False}
            return render(self.request, 'src/mpesa_payment.html', context)
        else:
            messages.warning(self.request, 'You have not added a billing address.')
            return redirect('src:checkout')
