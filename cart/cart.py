from django.conf import settings
from main.models import Product

'''Класс корзины '''

class Cart():

    '''функция инициализации сессии '''
    def __init__(self, request): # инициализирует поля нового объекта класса CART
        self.session = request.session # cохраняет сессию текущего пользователя в атрибут 'self.session' экземпляра класса, 
                                       # self.session — ссылка на объект сессии Django (request.session), через который происходит обмен данными с хранилищем сессии
        cart = self.session.get(settings.CART_SESSION_ID) # получает данные корзины из сессии с помощью метода get()
        if not cart: # если корзина (cart) пуста
            cart = self.session[settings.CART_SESSION_ID] = {} # Создаёт новую пустую корзину в виде словаря {}, Сохраняет этот словарь в сессии под ключом settings.CART_SESSION_ID, Присваивает его локальной переменной cart
        self.cart = cart # Сохраняет данные корзины (либо загруженные из сессии, либо только что созданные) в атрибут экземпляра self.cart, 
                         #Теперь объект класса Cart имеет прямой доступ к данным корзины через self.cart, что упрощает дальнейшую работу с ними (добавление товаров, подсчёт суммы и т. д.).
                         # self.cart — словарь с данными корзины (загруженный из сессии или созданный заново), где ключами обычно выступают ID товаров, а значениями — словари с параметрами (количество, цена и т. д.).
                         # Данные корзины (хранятся в self.cart) — обычно имеют структуру:
                                #{
                                 #   '1': {'quantity': 2, 'price': '19.99'},  # товар с ID=1, 2 шт.
                                 #   '5': {'quantity': 1, 'price': '45.50'},  # товар с ID=5, 1 шт.
                                 #   ...
                                #}
    
    '''функция добавления товаров '''
    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product.id not in self.cart:
            self.cart[product_id] = {'quantity':0, 'price': str(product.price)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    '''функция удаления товаров '''
    def remove(self, product):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    '''метод итерации, проходит по параметрам товаров в корзине и позволяет с ними работать'''
    def __iter__(self):
        product_ids = self.cart.keys() # возвращает специальный итерируемый объект типа dict_keys(['a', 'b', 'c']), динамически обновляется
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = float(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self): # возвращает общее количество единиц выбранных товаров
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self): # возвращает общую стоимость выбранных товаров
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self): # удаляет куки, связанные с текущей корзиной
        del self.session[settings.CART_SESSION_ID]
        self.save()
        

