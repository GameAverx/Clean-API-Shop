import json
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
import http.client


# conn = http.client.HTTPSConnection("httpbin.org")
# conn.request("GET", "/")
# r1 = conn.getresponse()
# print(r1.status, r1.reason)

def get_json_body(self):
    length = int(self.headers.get('Content-Length', 0))
    if length == 0:
        return {}
    return json.loads(self.rfile.read(length))

class SimpleHandler(BaseHTTPRequestHandler):
    def mainPage(self):
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response = b'<button>Buy</button>'
        return response
    def testpage(self):
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        # response = {'id': 42}
        # response =
        self.wfile.write(json.dumps({'error': 'Not found23'}, ensure_ascii=False).encode())
    def
    def do_GET(self):
        if self.path == '/':
            response = self.mainPage()
            self.wfile.write(response)
        elif self.path == '/about':
            response = self.testpage()
        elif self.path == '/register':

        #     response = b'<h1>Hell1</h1>'
        #     # print(BaseHTTPRequestHandler.client_address())x`x
        #     print('12323123')
        # else:
        #     response = b'<h1>Hell2</h1>'
        #     self.send_response(404)



    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(f'Получено: {post_data.decode()}'.encode())

# if __name__ == "__main__":
#     server = HTTPServer(('localhost', 8080), SimpleHandler)
#     with
server = HTTPServer(('localhost', 8080), SimpleHandler)

print("Сервер запущен на http://localhost:8080")
server.serve_forever()









# python -m http.server 8000
