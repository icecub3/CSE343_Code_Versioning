import json
import http.server
import socketserver

PORT = 8081

class ServerHandler(http.server.CGIHTTPRequestHandler):

    def do_POST(self):
      content_len = int(self.headers.get('Content-Length'))
      post_body = self.rfile.read(content_len)
      #print (post_body)

      json_string = post_body.decode('utf8').replace("'", '"')
      #print(json_string)

      #creates json object
      data = json.loads(json_string)
      #prints json object's properties part(like array accessing)
      print(data["properties"]["failure"])
      #converts json object to string
      s = json.dumps(data, indent=4, sort_keys=True)
      #prints the json file
      print (s)

      self.send_response(200)
      self.send_header("State", "Delivery Confirmed")
      self.end_headers()
      #sends response 
      self.wfile.write(post_body)

Handler = ServerHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
