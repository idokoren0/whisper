# File: scripts/terminator_service.py

import socket
import time
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    whisper_host = os.environ.get("WHISPER_HOST", "whisper")
    whisper_port = int(os.environ.get("WHISPER_PORT", 12345))
    termination_message = os.environ.get("TERMINATION_MESSAGE", "TERMINATE")

    logger.info(
        "Terminator service started. Waiting 20 seconds before sending termination message..."
    )
    time.sleep(20)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as terminator_socket:
            terminator_socket.connect((whisper_host, whisper_port))
            logger.info(f"Connected to Whisper server at {whisper_host}:{whisper_port}")
            logger.info(f"Sending termination message: {termination_message}")
            terminator_socket.sendall(termination_message.encode("utf-8"))
            logger.info("Termination message sent")
    except Exception as e:
        logger.error(f"Error connecting to Whisper server: {e}")


if __name__ == "__main__":
    main()
