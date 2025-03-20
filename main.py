import http.server
import socketserver
from lithic import Lithic
from datetime import datetime, timezone, timedelta

API_KEY = "YOUR_KEY_HERE"
CARD_TOKEN = "CARD_TOKEN"
ACCOUNT_TOKEN = "ACCOUNT_TOKEN"
CSS_URL = "https://brianclee-gh.github.io/card.css"

PORT = 8082

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "index.html"
        if self.path == "/get_embed_html":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()

            client = Lithic(
                api_key=API_KEY,
                environment="sandbox",
            )
            exp = datetime.now(timezone.utc) + timedelta(days=14)
            url = client.cards.get_embed_url(css=CSS_URL, token=CARD_TOKEN, expiration=exp)

            print(url)
            self.wfile.write(url)
            self.finish()
        elif self.path.endswith(".css"):
            self.send_response(200)
            self.send_header("Content-type", "text/css")
            self.end_headers()
            with open(self.path[1:], "rb") as f:
                self.wfile.write(f.read())
        else:
            super().do_GET()

Handler = MyHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
