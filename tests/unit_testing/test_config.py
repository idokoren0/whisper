import unittest
from src.config import Config

class TestConfig(unittest.TestCase):
    '''
    test that config values extraction 
    unit_test_config.yml yeild expected values 
    '''
    def setUp(self):
        self.config_file = 'tests/unit_testing/unit_test_config.yml'
        self.config = Config(self.config_file)
    
    def test_listening_port(self):
        self.assertEqual(self.config.port, 12345)
    
    def test_ip_address(self):
        self.assertEqual(self.config.ip_address, '0.0.0.0')
    
    def test_target_server(self):
        self.assertEqual(self.config.target_server, 'receiver')
    
    def test_target_port(self):
        self.assertEqual(self.config.target_port, 8080)

    def test_data_transfer_method(self):
        self.assertEqual(self.config.data_transfer, 'tcp')

if __name__ == '__main__':
    unittest.main()
