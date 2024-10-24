import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def create_stripe_product(title, description):
    """Создание продукта в Stripe"""
    return stripe.Product.create(name=title, description=description)

def create_stripe_price(product_id, amount, currency='usd'):
    """Создание цены для продукта в Stripe"""
    return stripe.Price.create(unit_amount=amount, currency=currency, product=product_id)

def create_stripe_checkout_session(price_id, success_url, cancel_url):
    """Создание сессии оформления заказа в Stripe"""
    return stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )