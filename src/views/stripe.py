import stripe
import random
import string

from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.views.generic import View

from src.models import Order, Payment

#   settings.STRIPE_SECRET_KEY
stripe.api_key = "sk_test_51ITWsHAtphnTyCFLHgmLpNhM5G1ue0XwrdT7" \
                 "pQveeGnb6QvOXGtIj0ZiUgDp30kmKCZ5wwyb8zXXakUTSunG1Nre00yGCp8WEf"
stripe_public = "pk_test_51ITWsHAtphnTyCFLGrC7BpCujwXqZ62816crdHGpiXH97" \
                "d1KhiQYtYDFGXWXawzFhXgDNq53dgoJwk2cb0zEqJEN00HLx8L8dZ"


def create_ref_code():
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=10))


class StripePaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        stripe_public_key = stripe_public
        if order.billing_address:
            context = {'order': order, 'DISPLAY_COUPON_FORM': False, 'stripe_public_key': stripe_public_key}
            return render(self.request, 'src/stripe.html', context)
        else:
            messages.warning(self.request, 'You have not added a billing address.')
            return redirect('src:checkout')

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total() * 100)
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="kes",
                source=token,
            )
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            order_products = order.products.all()
            order_products.update(ordered=True)
            for product in order_products:
                product.save()
            order.ordered = True
            order.ip = self.request.META.get('REMOTE_ADDR')
            order.payment = payment
            order.ref_code = create_ref_code()
            order.save()
            messages.success(self.request, "Your order was successful.")
            return redirect("src:track-order")

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.warning(self.request, f"{err.get('message')}")
            return redirect("/")
        except stripe.error.RateLimitError as e:
            messages.warning(self.request, f"Rate limit error.")
            return redirect("/")
        except stripe.error.InvalidRequestError as e:
            messages.warning(self.request, f"Invalid parameters.{e}")
            return redirect("/")
        except stripe.error.AuthenticationError as e:
            messages.warning(self.request, f"Not authenticated.{e}")
            return redirect("/")
        except stripe.error.APIConnectionError as e:
            messages.warning(self.request, "Network error")
            return redirect("/")
        except stripe.error.StripeError as e:
            messages.warning(self.request, "Something went wrong. You are not charged please try again.")
            return redirect("/")
        except Exception as e:
            messages.warning(self.request, f"A serious error occured we have been notified.{e}")
            return redirect("/")
