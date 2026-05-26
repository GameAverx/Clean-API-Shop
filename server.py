import json
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
import http.client
from urllib.parse import urlparse
import re
from handlers import auth, products, sellers, cart
from models import db_init
import jwt
from security import SECRET_KEY
import uuid

# conn = http.client.HTTPSConnection("httpbin.org")
# conn.request("GET", "/")
# r1 = conn.getresponse()
# print(r1.status, r1.reason)



class SimpleHandler(BaseHTTPRequestHandler):


    def send_json(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    def get_json_body(self):
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length))

    def get_session_id(self):
        cookies = self.headers.get('Cookie', '')
        session_id = None

        for cookie in cookies.split(';'):
            if 'session_id=' in cookie:
                session_id = cookie.split('=')[1].strip()
                break

        if not session_id:
            session_id = str(uuid.uuid4())
            self.send_header('Set-Cookie', f'session_id={session_id}; Path=/')

        return session_id

    def is_authentificate(self):
        user = self.headers.get('Authorization', '')
        if not user.startswith('Bearer '):
            return None
        token = user[7:]
        try:
            # для микросервисов нужно использвововать public_key.
            payload = jwt.decode(token,SECRET_KEY, algorithms= ['HS256'])
            return payload['user_id']
        except:
            return None

    # GET запросы
    def mainPage(self):
        result = products.tshirts_list(self)
        self.send_json(result[0], result[1])
    def shopPage(self, shop_id):
        # if self.path.startswith('/shopPage/'):
        #     parts = self.path.split('/')
        #     shop_id = parts[2]
        result = sellers.get_shop_page(shop_id)
        self.send_json(result[0], result[1])
    def productPage(self, product_id):
        result = products.get_product(product_id)
        self.send_json(result[0], result[1])
    # проверка оплаты заказа
    def complete_order(self, user_id, order_id):
        result = cart.complete_order(self, user_id, order_id)
        self.send_json(result[0], result[1])

    # POST запросы
    def sign_up(self):
        result = auth.register(self.get_json_body())
        self.send_json(result[0], result[1])

    def sign_in(self):
        result = auth.login(self.get_json_body())
        self.send_json(result[0], result[1])

    def add_product(self, user_id, shop_id):
        result = products.add_product(self,self.get_json_body(), user_id, shop_id)
        self.send_json(result[0], result[1])

    def new_seller(self):
        result = sellers.new_seller(self)
        self.send_json(result[0], result[1])

    def new_shop(self):
        result = sellers.new_shop(self, self.get_json_body())
        self.send_json(result[0], result[1])

    def add_to_cart(self, user_id, product_id=False):
        result = cart.add_to_cart(self, self.get_json_body(), user_id, product_id)
        self.send_json(result[0], result[1])

    # def new_cart(self, user_id, product_id):
    #     result = products.add_product(self, self.get_json_body(), user_id, product_id)
    #     self.send_json(result[0], result[1])

    # оплата корзины
    def purchase(self, user_id):
        result = cart.payment(self, user_id)
        self.send_json(result[0], result[1])

    # PUT запросы
    def edit_product(self, user_id, shop_id, product_id):
        # if self.path.startswith('/edit_product/'):
        #     parts = self.path.split('/')
        #     product_id = parts[2]
        result = products.edit_product(self, self.get_json_body(), user_id, shop_id, product_id)
        self.send_json(result[0], result[1])


    def update_cart(self, user_id, product_id=False):
        result = cart.update_cart(self, self.get_json_body(), user_id, product_id)
        self.send_json(result[0], result[1])

    # DELETE запросы
    def del_product(self, user_id, shop_id, product_id):
        result = products.del_product(self, user_id, shop_id, product_id)
        self.send_json(result[0], result[1])

    def clear_cart(self, user_id):
        result = cart.clear_cart(self, user_id)
        self.send_json(result[0], result[1])
    # типы запросов
    def do_GET(self):
        parsed = urlparse(self.path)

        match = re.match(r'^/user/(\d+)/order/([A-Z0-9]+)/complete$', self.path)
        if match:
            user_id = match.group(1)
            order_id = match.group(2)
            self.complete_order(user_id, order_id)

        if parsed.path == '/products':
            self.mainPage()
        elif self.path.startswith('/shopPage/'):
            parts = self.path.split('/')
            shop_id = parts[2]
            self.shopPage(shop_id)
        elif self.path.startswith('/productPage/'):
            parts = self.path.split('/')
            product_id = parts[2]
            self.productPage(product_id)
        else:
            self.send_json(404, {'error': 'Not found'})

    def do_POST(self):
        # добавления продукта /user/(\d+)/shop/(\d+)/product
        match = re.match(r'^/user/(\d+)/shop/(\d+)/product$', self.path)
        if match:
            user_id = match.group(1)
            shop_id = match.group(2)
            self.add_product(user_id, shop_id)
        # добавить в новую корзину несколько товаров
        match = re.match(r'^/user/(\d+)/cart$', self.path)
        if match:
            user_id = match.group(1)
            self.add_to_cart(user_id)
        match = re.match(r'^/user/(\d+)/cart/product/(\d+)$', self.path)
        if match:
            user_id = match.group(1)
            product_id = match.group(2)
            self.add_to_cart(user_id, product_id)
        match = re.match(r'^/user/(\d+)/cart/payment$', self.path)
        if match:
            user_id = match.group(1)
            self.purchase(user_id)

        elif self.path == '/register':
            self.sign_up()
        elif self.path == '/login':
            self.sign_in()
        # elif self.path == '/add_product':
        #     self.add_product()
        elif self.path == '/new_seller':
            self.new_seller()
        elif self.path == '/new_shop':
            self.new_shop()
        # elif self.path == '/edit_product/':
        #     self.edit_product()
        # elif self.path == '/del_product/':
        #     self.del_product()
        else:
            self.send_json(404, {'error': 'Not found'})

        # content_length = int(self.headers['Content-Length'])
        # post_data = self.rfile.read(content_length)
        #
        # self.send_response(200)
        # self.end_headers()
        # self.wfile.write(f'Получено: {post_data.decode()}'.encode())

    def do_PUT(self):
        # edit_product обновление продукта
        match = re.match(r'^/user/(\d+)/shop/(\d+)/product/(\d+)$', self.path)
        if match:
            user_id = match.group(1)
            shop_id = match.group(2)
            product_id = match.group(3)
            self.edit_product(user_id, shop_id, product_id)

        match = re.match(r'^/user/(\d+)/cart$', self.path)
        if match:
            user_id = match.group(1)
            self.update_cart(user_id)
        match = re.match(r'^/user/(\d+)/cart/product/(\d+)$', self.path)
        if match:
            user_id = match.group(1)
            product_id = match.group(2)
            self.update_cart(user_id, product_id)
        else:
            self.send_json(404, {'error': 'Not found'})

    def do_DELETE(self):
        # edit_product обновление продукта
        match = re.match(r'^/user/(\d+)/shop/(\d+)/product/(\d+)$', self.path)
        if match:
            user_id = match.group(1)
            shop_id = match.group(2)
            product_id = match.group(3)
            self.del_product(user_id, shop_id, product_id)
        match = re.match(r'^/user/(\d+)/cart$', self.path)
        if match:
            user_id = match.group(1)
            self.clear_cart(user_id)

        else:
            self.send_json(404, {'error': 'Not found'})

if __name__ == '__main__':
    db_init()
    server = HTTPServer(('localhost', 8080), SimpleHandler)
    print("Сервер запущен на http://localhost:8080")
    server.serve_forever()









# python -m http.server 8000
