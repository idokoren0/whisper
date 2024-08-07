import unittest
from unittest.mock import patch, MagicMock
from src.server import WhisperServer

class TestWhisperServer(unittest.TestCase):
    @patch('src.server.Config')
    @patch('src.server.DataProcessor')
    @patch('src.server.DataSender')
    def setUp(self, mock_data_sender, mock_data_processor, mock_config):
        self.mock_config = mock_config.return_value
        self.mock_data_processor = mock_data_processor.return_value
        self.mock_data_sender = mock_data_sender.return_value
        self.server = WhisperServer('config.yaml')

    @patch('src.server.socket.socket')
    def test_setup_server_socket(self, mock_socket):
        self.server.setup_server_socket()
        mock_socket.assert_called_once()
        mock_socket.return_value.bind.assert_called_once()
        mock_socket.return_value.listen.assert_called_once()

    # Add more tests for other methods...

if __name__ == '__main__':
    unittest.main()