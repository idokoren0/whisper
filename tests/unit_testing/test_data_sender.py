# import unittest
# from unittest.mock import patch, MagicMock
# from src.data_sender import DataSender
# from src.config import Config

# class TestDataSender(unittest.TestCase):
#     def setUp(self):
#         self.config = Config('tests/dummy_config.yml')
#         self.data_sender = DataSender(self.config)

#     @patch('src.data_sender.requests.post')
#     def test_send_data_http(self, mock_post):
#         enriched_data = '{"data": "test"}'
#         mock_post.return_value.status_code = 200
#         self.data_sender.send_data(enriched_data)
#         mock_post.assert_called_once()

#     @patch('src.data_sender.socket.socket')
#     @patch('src.data_sender.ssl.create_default_context')
#     def test_send_data_tcp(self, mock_create_default_context, mock_socket):
#         # Set up the config to use TCP
#         self.config.data_transfer = 'tcp'
#         enriched_data = '{"data": "test"}'
        
#         # Mock the SSL context to prevent file I/O during testing
#         mock_ssl_context = MagicMock()
#         mock_create_default_context.return_value = mock_ssl_context
#         mock_socket_inst = mock_socket.return_value
        
#         # Invoke the method under test
#         self.data_sender.send_data(enriched_data)
        
#         # Verify that the connect method was called
#         mock_socket_inst.connect.assert_called_once_with((self.config.target_server, self.config.target_port))
#         mock_socket_inst.sendall.assert_called_once_with(enriched_data.encode('utf-8'))

# if __name__ == '__main__':
#     unittest.main()