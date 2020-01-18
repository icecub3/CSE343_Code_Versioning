import json
import http.server
import socketserver

# json.dumps/dump -> creates json file
# json.loads/load -> parses json file
PORT = 8081


class ServerHandler(http.server.CGIHTTPRequestHandler):

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        # bytewise json file
        json_body = self.rfile.read(content_len)
        print(json_body)
        # parses json file
        data = json.loads(json_body)
        # prints json object's properties,failure part(like array accessing)
        print(data['origin'])

        # Start of operations

        # TR:
        # Plan grubundan gelen request'lerin alanlarındaki değerlere bakıp yapılacak işleme karar vereceğiz.
        # Gerekli fonksiyonları çağırıp işlemleri tamamlayacağız.
        # İşlemlerin sonucunu bir JSON nesnesine yazıp, response olarak bu nesneyi Plan grubuna göndereceğiz.

        # ENG:
        #   This is where we operate on the incoming request, we need to decide what request wants from us
        # like commit, merge, rollback etc.
        #   We need to call necessary functions and perform operations here
        #   After all the needed operations performed, we will send the result(response) as a JSON object
        # TODO: Check the information on the incoming request.
        # TODO: Decide what operation we should perform
        # TODO: Call that function and save its result.
        # TODO: Send the result of the operation as an HTTP Response in JSON format

        # End of operations

        # Send the response after finishing all the operation needed
        self.send_response(200)
        self.send_header("State", "Delivery Confirmed")
        self.end_headers()
        # sends response itself
        self.wfile.write(json_body)


Handler = ServerHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()


def commit():
    # TODO: Add parameters needed.
    # TODO: Perform commit by calling the appropriate function from the GIT Library we use.
    return 0


def merge():
    # TODO: Add parameters needed.
    # TODO: Perform merge by calling the appropriate function from the GIT Library we use.
    return 0


def rollback():
    # TODO: Add parameters needed.
    # TODO: Ggo back to previous version by calling the appropriate function from the GIT Library we use.
    return 0
