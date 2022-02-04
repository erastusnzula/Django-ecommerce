from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from src.models import Order, Refund
from src.forms import RefundForm


class RefundView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        refund = Refund.objects.filter(user=self.request.user).order_by('date_req')
        email = self.request.user.email
        form = RefundForm()
        context = {'form': form,
                   'object': refund,
                   'email': email,
                   }
        return render(self.request, 'src/request_refund.html', context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            try:
                order = Order.objects.get(user=self.request.user, ref_code=ref_code, refund_granted=False,
                                          received=False, refund_requested=False, being_delivered=False)
                order.refund_requested = True
                order.save()
                refund = Refund()
                refund.user = self.request.user
                refund.order = order
                refund.reason = message
                refund.email = self.request.user.email
                refund.ref_code = ref_code
                refund.save()
                messages.info(self.request,
                              f'You refund request was received. We will contact you via email: {self.request.user.email}')
                return redirect('src:request-refund')
            except ObjectDoesNotExist:
                messages.info(self.request, 'Refund denied.')
                return redirect('src:request-refund')
