import json
import http.server
import socketserver

#json.dumps/dump -> creates json file
#json.loads/load -> parses json file
PORT = 8081

class ServerHandler(http.server.CGIHTTPRequestHandler):

    def do_POST(self):
      content_len = int(self.headers.get('Content-Length'))
      #bytewise json file
      json_body = self.rfile.read(content_len)
      print(json_body)
      #parses json file
      data = json.loads(json_body)
      #prints json object's properties,failure part(like array accessing)
      print(data["properties"]["failure"])

      self.send_response(200)
      self.send_header("State", "Delivery Confirmed")
      self.end_headers()
      #sends response itself
      self.wfile.write(json_body)

Handler = ServerHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
