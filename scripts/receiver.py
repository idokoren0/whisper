import socket
import threading
import logging

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

def main():
    listen_host = '0.0.0.0'
    listen_port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((listen_host, listen_port))
    server_socket.listen(5)
    logger.info(f'Receiver server listening on {listen_host}:{listen_port}')

    while True:
        client_socket, addr = server_socket.accept()
        logger.info(f'Connection from {addr} has been established.')
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == '__main__':
    main()