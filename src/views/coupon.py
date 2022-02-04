from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.conf import settings
from django.views.generic import View

import stripe

from src.models import Order, Coupon
from src.forms import CouponForm

stripe.api_key = "sk_test_51ITWsHAtphnTyCFLHgmLpNhM5G1ue0XwrdT7" \
                 "pQveeGnb6QvOXGtIj0ZiUgDp30kmKCZ5wwyb8zXXakUTSunG1Nre00yGCp8WEf"


def get_coupon(request, code):
    """Display coupon information."""
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, 'This coupon does not exist.')
        return redirect('src:checkout')


class AddCoupon(View):
    def post(self, *args, **kwargs):
        """Allow user input form coupon data."""
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.info(self.request, 'Successfully added coupon')
                return redirect('src:checkout')
            except:
                return redirect('src:checkout')
