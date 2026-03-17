from django.conf import settings
from main.models import Product

class Cart():

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product.id not in self.cart:
            self.cart[product_id] = {'quantity':0, 'price': str(product.price)}