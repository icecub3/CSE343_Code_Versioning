import json
import http.server
import socketserver

PORT = 8081

class ServerHandler(http.server.CGIHTTPRequestHandler):

    def do_POST(self):
      content_len = int(self.headers.get('Content-Length'))
      post_body = self.rfile.read(content_len)
      print (post_body)
      #json_string = json.dumps(post_body)
      #print (json_string)
      
      self.send_response(200)
      self.send_header("Content-type", "")
      self.end_headers()
      #self.wfile.write(json.dumps("njcs"))

Handler = ServerHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
