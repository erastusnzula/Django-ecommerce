from django.contrib import admin
from django.utils.html import format_html
#   from django.contrib.auth.models import Group

from .models import Product, CartProduct, Order, Address, Payment, Coupon, Refund, Setting, ProductImages, Profile, \
    Contact, Category, Size
from src.models.article import ArticleCategory, Article, Comment


# admin.site.unregister(Group)


class ProductImageModel(admin.StackedInline):
    model = ProductImages


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_image', 'price', 'discount_price', 'slug', 'label']
    inlines = [ProductImageModel]
    list_per_page = 3

    def product_image(self, obj):
        return format_html(f'''
            <img height='80px' src='{obj.image.url}'/>
        ''')


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(cancelled=True, refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


def make_product_received(modeladmin, request, queryset):
    queryset.update(received=True)


make_product_received.short_description = 'Update orders to received'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered', 'ordered_date', 'being_delivered', 'cancelled', 'received', 'refund_requested',
                    'refund_granted',
                    'billing_address', 'shipping_address', 'payment', 'coupon', 'ip']
    list_filter = ['ordered', 'being_delivered', 'received', 'refund_requested', 'refund_granted']
    list_display_links = ['user', 'billing_address', 'shipping_address', 'payment', 'coupon']
    search_fields = ['user__username', 'ref_code']
    actions = [make_refund_accepted, make_product_received]
    readonly_fields = ['user', 'ordered', 'billing_address', 'shipping_address', 'payment', 'coupon', 'ref_code',
                       'products', 'ordered_date']
    date_hierarchy = 'ordered_date'
    fieldsets = [
        ('Name', {'fields': ['user', 'ip', 'billing_address', 'shipping_address']}),
        ('Order Information', {'fields': ['ordered', 'ordered_date', 'payment', 'coupon', 'ref_code']}),
        ('Ordered Items', {'fields': ['products']}),
        ('Delivery Status', {'fields': ['being_delivered', 'cancelled', 'received']}),
        ('Refund', {'fields': ['refund_requested', 'refund_granted']}),
    ]


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'ordered']
    readonly_fields = ['user', 'product', 'quantity', 'ordered']
    list_per_page = 5


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'address', 'town', 'country', 'zip', 'address_type', 'default']
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']
    date_hierarchy = 'date'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    readonly_fields = ['stripe_charge_id', 'paypal_order_key', 'paypal_user_id', 'user', 'paypal_full_name',
                       'paypal_email', 'paypal_address1', 'paypal_address2', 'paypal_postal_code',
                       'paypal_country_code', 'amount', 'paypal_amount']
    list_display = ['user', 'amount', 'timestamp']
    list_per_page = 5
    date_hierarchy = 'timestamp'
    fieldsets = (
        ('Customer', {'fields': ['user']}),
        ('Stripe Payment', {'fields': ['stripe_charge_id']}),
        ('Paypal Payment', {'fields': ['paypal_order_key', 'paypal_user_id', 'paypal_full_name',
                                       'paypal_email', 'paypal_address1', 'paypal_address2', 'paypal_postal_code',
                                       'paypal_country_code',
                                       'paypal_amount']}),
        ('Total Amount Paid', {'fields': ['amount']}),

    )


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    pass


def refund_accepted(modeladmin, request, queryset):
    queryset.update(accepted=True)


refund_accepted.short_description = 'Update refund to accepted'


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ['order', 'ref_code', 'accepted', 'email', 'date_req']
    readonly_fields = ['order', 'ref_code', 'accepted', 'email', 'reason']
    actions = [refund_accepted]
    date_hierarchy = 'date_req'


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User Profile', {'fields': ['user', 'country', 'phone_number']}),
        ('Profile Photo', {'fields': ['image']}),
    ]
    readonly_fields = ['user', 'country', 'phone_number', 'image']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
admin.site.site_title = "EMU"
admin.site.site_header = "EMU"
admin.site.index_title = "Administration"
