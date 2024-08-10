# import unittest
# from unittest.mock import patch, MagicMock, call
# from src.server import WhisperServer

# class TestWhisperServer(unittest.TestCase):

#     @patch('src.server.Config')
#     @patch('src.server.DataProcessor')
#     @patch('src.server.DataSender')
#     def setUp(self, mock_data_sender, mock_data_processor, mock_config):
#         # Setup mock objects
#         self.mock_config = mock_config.return_value
#         self.mock_data_processor = mock_data_processor.return_value
#         self.mock_data_sender = mock_data_sender.return_value
#         self.server = WhisperServer('tests/dummy_config.yml')
    
#     @patch('src.server.socket.socket')
#     def test_setup_server_socket(self, mock_socket):
#         # Test the setup of the server socket
#         self.server.setup_server_socket()
#         mock_socket.assert_called_once()
#         mock_socket.return_value.bind.assert_called_once_with((self.mock_config.ip_address, self.mock_config.port))
#         mock_socket.return_value.listen.assert_called_once()

#     @patch('src.server.socket.socket')
#     @patch('threading.Thread')
#     def test_listen_for_connections(self, mock_thread, mock_socket):
#         # Setup the server socket
#         mock_socket_inst = mock_socket.return_value
#         self.server.setup_server_socket()
        
#         # Mock accept to simulate a client connection
#         mock_socket_inst.accept.return_value = (MagicMock(), ('127.0.0.1', 50000))
        
#         # Run the method under test
#         with patch.object(self.server, 'is_running', True):
#             self.server.listen_for_connections()
        
#         # Verify that accept was called and a new thread was started to handle the client
#         mock_socket_inst.accept.assert_called_once()
#         mock_thread.assert_called_once()

#     @patch('src.server.socket.socket')
#     def test_handle_client(self, mock_socket):
#         # Mock client socket and its recv method
#         mock_client_socket = MagicMock()
#         mock_client_socket.recv.return_value = b"test data"
#         mock_address = ('127.0.0.1', 50000)

#         # Mock data processor's enrich_data
#         self.mock_data_processor.enrich_data.return_value = '{"data": "test"}'

#         # Run the method under test
#         self.server.handle_client(mock_client_socket, mock_address)

#         # Verify that recv and send_data were called
#         mock_client_socket.recv.assert_called()
#         self.mock_data_sender.send_data.assert_called_once_with('{"data": "test"}')
#         mock_client_socket.close.assert_called_once()

#     def test_receive_data(self):
#         # Mock client socket and its recv method
#         mock_client_socket = MagicMock()
#         mock_client_socket.recv.side_effect = [b"part1", b"part2", b""]  # Simulate two chunks followed by an empty packet

#         # Run the method under test
#         result = self.server.receive_data(mock_client_socket)

#         # Verify that recv was called multiple times and the data was correctly assembled
#         self.assertEqual(result, b"part1part2")

#     @patch('src.server.socket.socket')
#     def test_start(self, mock_socket):
#         # Mock methods called within start
#         with patch.object(self.server, 'setup_server_socket') as mock_setup, \
#              patch.object(self.server, 'listen_for_connections') as mock_listen:
#             self.server.start()
        
#         # Verify that setup and listen methods were called
#         mock_setup.assert_called_once()
#         mock_listen.assert_called_once()
#         self.assertTrue(self.server.is_running)

#     @patch('src.server.socket.socket')
#     def test_stop(self, mock_socket):
#         # Mock the server socket and call stop
#         mock_socket_inst = mock_socket.return_value
#         self.server.start()  # Start the server to set up the socket
#         self.server.stop()

#         # Verify that the server socket was closed and is_running is set to False
#         mock_socket_inst.close.assert_called_once()
#         self.assertFalse(self.server.is_running)

# if __name__ == '__main__':
#     unittest.main()
