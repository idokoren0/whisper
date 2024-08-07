import socket
import requests
import logging

class DataSender:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def send_data(self, enriched_data):
        if self.config.use_http:
            self.send_data_http(enriched_data)
        else:
            self.send_data_tcp(enriched_data)

    def send_data_http(self, enriched_data):
        try:
            response = requests.post(f"http://{self.config.target_server}:{self.config.target_port}", json=enriched_data)
            response.raise_for_status()
            self.logger.info("Data sent successfully via HTTP")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error sending data via HTTP: {e}")

    def send_data_tcp(self, enriched_data):
        target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            target_socket.connect((self.config.target_server, self.config.target_port))
            target_socket.sendall(enriched_data.encode('utf-8'))
            self.logger.info("Data sent successfully via TCP")
        except Exception as e:
            self.logger.error(f"Error sending data via TCP: {e}")
        finally:
            target_socket.close()