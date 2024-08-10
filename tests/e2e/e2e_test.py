import unittest
import subprocess
import time

class TestE2E(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start the services using docker-compose
        subprocess.run(["pwd"])
        subprocess.run(["ls", "l"])
        subprocess.run(["docker-compose", "-f", "docker-compose.e2e.yml", "up", "-d"])
        # Allow some time for services to start
        time.sleep(10)

    @classmethod
    def tearDownClass(cls):
        # Stop the services and clean up
        subprocess.run(["docker-compose", "-f", "docker-compose.e2e.yml", "down"])

    def test_message_flow(self):
        # Wait a bit to ensure the message flow has happened
        time.sleep(5)

        # Fetch logs from the receiver container
        result = subprocess.run(
            ["docker-compose", "-f", "docker-compose.e2e.yml", "logs", "receiver"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        # Check if the expected message is in the logs
        logs = result.stdout
        expected_message = "Hello Whisper, this is a test message!"

        self.assertIn(expected_message, logs, "The expected message was not found in the receiver's logs.")

if __name__ == '__main__':
    unittest.main()
