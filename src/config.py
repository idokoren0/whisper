import yaml


class Config:
    def __init__(self, config_file):
        """
        Extract confing values from yaml file
        """
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)
        self.port = config["listening_port"]
        self.ip_address = "0.0.0.0"
        self.target_server = config["target_server"]
        self.target_port = config["target_port"]
        self.data_transfer = config.get("data_transfer", "tcp")
        self.terminator_message = config["terminator"]["terminator_message"]
        self.terminator_ip = config["terminator"]["terminator_ip"]
