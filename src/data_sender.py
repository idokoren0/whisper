import socket
import ssl
import logging
import requests


class DataSender:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def send_data(self, enriched_data):
        if self.config.data_transfer == "http":
            self.send_data_http(enriched_data)
        elif self.config.data_transfer == "tcp":
            self.send_data_tcp(enriched_data)
        else:
            self.logger.error(
                f"Unknown data transfer method: {self.config.data_transfer}"
            )

    def send_data_http(self, enriched_data):
        try:
            response = requests.post(
                f"https://{self.config.target_server}:{self.config.target_port}",
                json=enriched_data,
                verify="/app/server.crt",  # Make sure to use the correct path to your server certificate
            )
            response.raise_for_status()
            self.logger.info("Data sent successfully via HTTPS")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error sending data via HTTPS: {e}")

    def send_data_tcp(self, enriched_data):
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_verify_locations("/app/server.crt")

        target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            wrapped_socket = context.wrap_socket(
                target_socket, server_hostname=self.config.target_server
            )
            wrapped_socket.connect((self.config.target_server, self.config.target_port))
            wrapped_socket.sendall(enriched_data.encode("utf-8"))
            self.logger.info("Data sent successfully via TCP with TLS")
        except Exception as e:
            self.logger.error(f"Error sending data via TCP with TLS: {e}")
        finally:
            wrapped_socket.close()
