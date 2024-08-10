import unittest
import subprocess
import time

class TestE2E(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start the services using docker-compose
        subprocess.run(["docker-compose", "up", "-d"], check=True)

        time.sleep(10)

    def poll_logs_for_message(self, container, expected_message, timeout=30):
        """Poll the logs of a container until the expected message is found or timeout occurs."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = subprocess.run(
                ["docker-compose", "logs", container],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            logs = result.stdout
            print(logs)

            if expected_message in logs:
                return True
            time.sleep(1)
        return False

    def test_message_flow(self):

        # Poll logs until the expected message is found or timeout occurs
        expected_message = "Hello Whisper, this is a test message!"
        found = self.poll_logs_for_message("receiver", expected_message)

        self.assertTrue(found, "The expected message was not found in the receiver's logs.")
    
    @classmethod
    def tearDownClass(cls):
        # Stop the services and clean up
        subprocess.run(["docker-compose", "down", "--volumes", "--remove-orphans"], check=True)


if __name__ == '__main__':
    unittest.main()