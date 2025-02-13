import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class HttpRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        ...


    def do_POST(self):
        ...



def run_server():
    server = HTTPServer(("127.0.0.1", 8000), HttpRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    run_server()