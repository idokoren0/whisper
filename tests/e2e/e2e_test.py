import unittest
import subprocess
import time

class TestE2E(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start the services using docker-compose
        subprocess.run(["docker-compose", "up", "-d"], check=True)
        # Allow some time for services to start
        time.sleep(10)

    @classmethod
    def tearDownClass(cls):
        # Stop the services and clean up
        subprocess.run(["docker-compose", "down", "--volumes", "--remove-orphans"], check=True)

        # Fetch logs after the services have been stopped
        cls.logs = cls.get_logs("receiver")

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
        # Perform the log check after services have been stopped
        expected_message = "Hello Whisper, this is a test message!"

        # Print logs for debugging purposes
        print(self.logs)

        # Check if the expected message is in the logs
        self.assertIn(expected_message, self.logs, "The expected message was not found in the receiver's logs.")

if __name__ == '__main__':
    unittest.main()
