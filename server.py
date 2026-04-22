import json
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
import http.client
from handlers import auth, products
from models import db_init

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

    # GET запросы
    def mainPage(self):
        result = products.tshirts_list(self)
        self.send_json(result[0], result[1])

    # POST запросы
    def sign_up(self):
        result = auth.register(self.get_json_body())
        self.send_json(result[0], result[1])

    def sign_in(self):
        result = auth.login(self.get_json_body())
        self.send_json(result[0], result[1])

    # типы запросов
    def do_GET(self):
        if self.path == '/':
            self.mainPage()
        else:
            self.send_json(404, {'error': 'Not found'})

    def do_POST(self):
        if self.path == '/register':
            self.sign_up()
        elif self.path == '/login':
            self.sign_in()
        else:
            self.send_json(404, {'error': 'Not found'})

        # content_length = int(self.headers['Content-Length'])
        # post_data = self.rfile.read(content_length)
        #
        # self.send_response(200)
        # self.end_headers()
        # self.wfile.write(f'Получено: {post_data.decode()}'.encode())
    def do_PUT(self):
        pass

    def do_DELETE(self):
        pass

if __name__ == '__main__':
    db_init()
    server = HTTPServer(('localhost', 8080), SimpleHandler)
    print("Сервер запущен на http://localhost:8080")
    server.serve_forever()









# python -m http.server 8000
