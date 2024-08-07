import socket
import threading
import logging
from .data_processor import DataProcessor
from .data_sender import DataSender
from .config import Config

class WhisperServer:
    def __init__(self, config_file):
        self.config = Config(config_file)
        self.data_processor = DataProcessor()
        self.data_sender = DataSender(self.config)
        self.server_socket = None
        self.is_running = False
        self.logger = logging.getLogger(__name__)

    def start(self):
        self.is_running = True
        self.setup_server_socket()
        self.logger.info(f"Whisper started, listening on {self.config.ip_address}:{self.config.port}")
        self.listen_for_connections()

    def setup_server_socket(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.config.ip_address, self.config.port))
            self.server_socket.listen(5)
        except Exception as e:
            self.logger.error(f"Error setting up server socket: {e}")
            raise

    def listen_for_connections(self):
        while self.is_running:
            try:
                client_socket, address = self.server_socket.accept()
                self.logger.info(f"Connection from {address} has been established.")
                threading.Thread(target=self.handle_client, args=(client_socket, address)).start()
            except Exception as e:
                self.logger.error(f"Error accepting client connection: {e}")

    def handle_client(self, client_socket, address):
        try:
            message = self.receive_data(client_socket)
            if message:
                enriched_data = self.data_processor.enrich_data(message, address)
                self.data_sender.send_data(enriched_data)
        except Exception as e:
            self.logger.error(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()

    def receive_data(self, client_socket):
        data = b''
        while True:
            try:
                packet = client_socket.recv(4096)
                if not packet:
                    break
                data += packet
            except Exception as e:
                self.logger.error(f"Error receiving data: {e}")
                break
        return data

    def stop(self):
        self.is_running = False
        if self.server_socket:
            self.server_socket.close()
        self.logger.info("Whisper stopped")

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Start the Whisper server.')
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to the configuration file.')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    whisper_server = WhisperServer(args.config)
    try:
        whisper_server.start()
    except KeyboardInterrupt:
        whisper_server.stop()
        print("Whisper stopped")

if __name__ == "__main__":
    main()