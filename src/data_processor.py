import time
import hashlib
import json


class DataProcessor:
    def enrich_data(self, message, address):
        """
        Process message from source and enrich with
        requierd fields
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        client_ip, client_port = address
        md5_hash = hashlib.md5(message).hexdigest()
        enriched_message = {
            "timestamp": timestamp,
            "client_ip": client_ip,
            "client_port": client_port,
            "md5_hash": md5_hash,
            "data": message.decode("utf-8"),
        }
        return json.dumps(enriched_message)
