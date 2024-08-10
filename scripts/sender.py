import socket
import os
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    target_host = os.environ.get('WHISPER_HOST', 'localhost')
    target_port = int(os.environ.get('WHISPER_PORT', 12345))
    message = 'Hello There'

    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((target_host, target_port))
                logger.info(f'Connected to Whisper server at {target_host}:{target_port}')
                client_socket.sendall(message.encode('utf-8'))
                logger.info('Sent message: %s', message)
        except Exception as e:
            logger.error(f'Error connecting to Whisper server: {e}')
        time.sleep(5)  # Wait for 5 seconds before sending the next message

if __name__ == '__main__':
    main()