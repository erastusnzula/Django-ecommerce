import random
import string
import json

from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
from paypalcheckoutsdk.orders import OrdersGetRequest

from src.models import Payment
from src.models.order import Order


def create_ref_code():
    """Generate a random reference code."""
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=10))


class PaypalPayment(View):
    """Paypal's payment class."""

    def get(self, *args, **kwargs):
        """Display paypal's order content."""
        order = Order.objects.get(user=self.request.user, ordered=False)
        amount = int(order.get_total() / 100)
        if order.billing_address:
            context = {'order': order, 'DISPLAY_COUPON_FORM': False, 'amount': amount}
            return render(self.request, 'src/paypal.html', context)
        else:
            messages.warning(self.request, 'You have not added a billing address.')
            return redirect('src:checkout')


class PayPalClient:
    """Paypal client access login details."""

    def __init__(self):
        """Initialize the class attributes."""
        self.client_id = "AaOM6adDF59berGM_rTpmEeo55imiiI2NYJlydVwpyi0ohhPhUxz6c_N0Cq9mKzjhQml5eLpYvn2ZZIv"
        self.client_secret = "EKXp-l8j0HQtwZArX1j1pxC_zuiUmVKCjQG6kMJmstapHs2JYxA0yIQkrBINr9U_mNh3KRIcT03gT0tF"
        # self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.environment = LiveEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)


def paypal_payment_complete(request):
    """Steps to be executed upon a successful payment."""
    try:
        PPClient = PayPalClient()
        body = json.loads(request.body)
        data = body["orderID"]
        user_id = request.user.id
        requestorder = OrdersGetRequest(data)
        response = PPClient.client.execute(requestorder)
        paypal_amount = response.result.purchase_units[0].amount.value
        order = Order.objects.get(user=request.user, ordered=False)

        #   Send payment details to backend.
        payment = Payment()
        payment.user = request.user
        payment.amount = order.get_total()
        payment.paypal_amount = paypal_amount
        payment.paypal_email = response.result.payer.email_address
        payment.paypal_country_code = response.result.purchase_units[0].shipping.address.country_code
        payment.paypal_address1 = response.result.purchase_units[0].shipping.address.address_line_1
        payment.paypal_address2 = response.result.purchase_units[0].shipping.address.admin_area_2
        payment.paypal_full_name = response.result.purchase_units[0].shipping.name.full_name
        payment.paypal_postal_code = response.result.purchase_units[0].shipping.address.postal_code
        payment.paypal_order_key = response.result.id
        payment.paypal_user_id = user_id
        payment.save()

        order_products = order.products.all()
        order_products.update(ordered=True)
        for product in order_products:
            product.save()
        order.ordered = True
        order.ip = request.META.get('REMOTE_ADDR')
        order.payment = payment
        order.ref_code = create_ref_code()
        order.save()
        messages.success(request,
                         f"Order: ({create_ref_code()} ) successfully submitted. Thank you for shopping with us.")
        return JsonResponse("Payment completed!", safe=False)
    except Exception:
        messages.warning(request, "Payment not successful.")
