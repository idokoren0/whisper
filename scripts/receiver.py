import socket
import threading
import logging
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_client(client_socket):
    try:
        data = client_socket.recv(4096)
        logger.info(f'Received enriched data: {data.decode("utf-8")}')
    except Exception as e:
        logger.error(f'Error receiving data: {e}')
    finally:
        client_socket.close()

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        logger.info(f'Received enriched data via HTTP: {post_data.decode("utf-8")}')
        self.send_response(200)
        self.end_headers()

def start_tcp_server(listen_host, listen_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((listen_host, listen_port))
    server_socket.listen(5)
    logger.info(f'Receiver server listening on {listen_host}:{listen_port} (TCP)')
    while True:
        client_socket, addr = server_socket.accept()
        logger.info(f'Connection from {addr} has been established.')
        threading.Thread(target=handle_client, args=(client_socket,)).start()

def start_http_server(listen_host, listen_port):
    server = HTTPServer((listen_host, listen_port), SimpleHTTPRequestHandler)
    logger.info(f'Receiver server listening on {listen_host}:{listen_port} (HTTP)')
    server.serve_forever()

def main():
    listen_host = '0.0.0.0'
    listen_port = 8080
    use_http = os.environ.get('USE_HTTP', 'false').lower() == 'true'

    if use_http:
        start_http_server(listen_host, listen_port)
    else:
        start_tcp_server(listen_host, listen_port)

if __name__ == '__main__':
    main()
