import unittest
import subprocess
import time

class TestE2E(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize logs attribute to avoid AttributeError
        cls.logs = ""

        # Start the services using docker-compose
        subprocess.run(["docker-compose", "up", "-d"], check=True)
        # Allow some time for services to start
        time.sleep(10)

    @classmethod
    def tearDownClass(cls):
        # Fetch logs before stopping the services
        try:
            cls.logs = cls.get_logs("receiver")
        except Exception as e:
            print(f"Error fetching logs: {e}")
            cls.logs = ""

        # Stop the services and clean up
        subprocess.run(["docker-compose", "down", "--volumes", "--remove-orphans"], check=True)

    @classmethod
    def get_logs(cls, container):
        """Fetch logs from a specific container."""
        result = subprocess.run(
            ["docker-compose", "logs", container],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            check=True
        )
        return result.stdout

    def test_message_flow(self):
        # Access logs captured in tearDownClass
        logs = self.__class__.logs

        # Print logs for debugging purposes
        print(logs)

        # Expected message in logs
        expected_message = "Hello Whisper, this is a test message!"

        # Check if the expected message is in the logs
        self.assertIn(expected_message, logs, "The expected message was not found in the receiver's logs.")

if __name__ == '__main__':
    unittest.main()