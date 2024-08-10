import socket
import ssl
import threading
import logging
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_client(client_socket):
    try:
        data = client_socket.recv(4096)
        logger.info(f'Received enriched data: {data.decode("utf-8")}')
    except Exception as e:
        logger.error(f"Error receiving data: {e}")
    finally:
        client_socket.close()


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        logger.info(f'Received enriched data via HTTPS: {post_data.decode("utf-8")}')
        self.send_response(200)
        self.end_headers()


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


def start_tcp_server(listen_host, listen_port):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="/app/server.crt", keyfile="/app/server.key")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((listen_host, listen_port))
    server_socket.listen(5)
    logger.info(
        f"Receiver server listening on {listen_host}:{listen_port} (TCP with TLS)"
    )
    while True:
        client_socket, addr = server_socket.accept()
        logger.info(f"Connection from {addr} has been established.")
        wrapped_socket = context.wrap_socket(client_socket, server_side=True)
        threading.Thread(target=handle_client, args=(wrapped_socket,)).start()


def start_http_server(listen_host, listen_port):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="/app/server.crt", keyfile="/app/server.key")

    httpd = ThreadingSimpleServer((listen_host, listen_port), SimpleHTTPRequestHandler)
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    logger.info(f"Receiver server listening on {listen_host}:{listen_port} (HTTPS)")
    httpd.serve_forever()


def main():
    listen_host = "0.0.0.0"
    listen_port = 8080
    data_transfer = os.environ.get("DATA_TRANSFER", "tcp")

    if data_transfer == "tcp":
        start_tcp_server(listen_host, listen_port)
    elif data_transfer == "http":
        start_http_server(listen_host, listen_port)
    else:
        logger.error(f"Unsuppored data transfer method: {data_transfer}")


if __name__ == "__main__":
    main()
