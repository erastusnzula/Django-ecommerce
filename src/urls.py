from django.urls import path
from src.views.stripe import StripePaymentView
from src.views.refund import RefundView
from src.views.coupon import AddCoupon
from src.views.product_details import ProductDetail
from src.views.home import HomeView
from src.views.cart import add_to_cart, remove_single_product_from_cart, remove_from_cart, add_to_cart_home, \
    add_to_cart_product, remove_from_cart_product, remove_product_home, adjust_cart_quantity_home
from src.views.checkout import CheckoutView
from src.views.cartsummary import CartSummary
from src.views.mpesapayment import MpesaPayment
from src.views.track_order import TrackOrder
from src.views.search import SearchProduct
from src.views.setting import Setting
from src.views.profile import UserProfileUpdate, delete_profile, delete_account
from src.views.contact import ContactAdmin, ContactConfirmation
from src.views.paypal import PaypalPayment, paypal_payment_complete
from src.views.category import product_category
from src.views.size import product_size, SelectSize
from src.views.article import Articles, ArticleDetails,article_category

app_name = 'src'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('profile/', UserProfileUpdate.as_view(), name='profile'),
    path('product/<slug>/', ProductDetail.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-to-cart-home/<slug>/', add_to_cart_home, name='add-to-cart-home'),
    path('add-to-cart-product/<slug>/', add_to_cart_product, name='add-to-cart-product'),
    path('add-coupon/', AddCoupon.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-from-cart-product/<slug>/', remove_from_cart_product, name='remove-from-cart-product'),
    path('remove-single-product-from-cart/<slug>/', remove_single_product_from_cart,
         name='remove-single-product-from-cart'),
    path('remove-product-home/<slug>/', remove_product_home,
         name='remove-product-home'),
    path('adjust-cart-product-home/<slug>/', adjust_cart_quantity_home,
         name='adjust-cart-product-home'),
    path('cart-summary/', CartSummary.as_view(), name='cart-summary'),
    path('track-order/', TrackOrder.as_view(), name='track-order'),
    path('stripe/<payment_option>/', StripePaymentView.as_view(), name='stripe'),
    path('mpesa-payment/<payment_option>/', MpesaPayment.as_view(), name='mpesa-payment'),
    path('paypal/<payment_option>/', PaypalPayment.as_view(), name='paypal'),
    path('payment_complete/', paypal_payment_complete, name='paypal-payment-complete'),
    path('request-refund/', RefundView.as_view(), name='request-refund'),
    path('search/', SearchProduct.as_view(), name='search'),
    path('about/', Setting.as_view(), name='setting'),
    path('contact/', ContactAdmin.as_view(), name='contact'),
    path('contact-confirm/', ContactConfirmation.as_view(), name='contact-confirm'),
    path('delete-profile/', delete_profile, name='delete-profile'),
    path('delete-account/', delete_account, name='delete-account'),
    path('<category>/', product_category, name='category'),
    path('size/<size>/', product_size, name='size'),
    path('size-select/<slug>/', SelectSize.as_view(), name='size-select'),
    path('emu/articles/', Articles.as_view(), name='articles'),
    path('article/<slug>/', ArticleDetails.as_view(), name='article-details'),
    path('emu/article/<category>/', article_category, name='article-category'),

]
