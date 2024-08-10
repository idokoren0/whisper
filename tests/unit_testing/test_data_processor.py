import unittest
from unittest.mock import patch
from src.data_processor import DataProcessor
import time
import hashlib
import json

class TestDataProcessor(unittest.TestCase):

    def setUp(self):
        self.data_processor = DataProcessor()

    @patch('time.strftime')
    def test_enrich_data(self, mock_strftime):
        '''
        check that data processing results in expected values
        '''
        mock_strftime.return_value = '2024-08-09 12:34:56'
        
        message = b"Hello, world!"
        address = ('0.0.0.0', 12345)
        
        result = self.data_processor.enrich_data(message, address)
        
        expected_md5 = hashlib.md5(message).hexdigest()
        expected_data = {
            'timestamp': '2024-08-09 12:34:56',
            'client_ip': '0.0.0.0',
            'client_port': 12345,
            'md5_hash': expected_md5,
            'data': message.decode('utf-8')
        }
        expected_result = json.dumps(expected_data)
        
        self.assertEqual(result, expected_result)

    def test_md5_hash(self):
        '''
        Test that the MD5 hash is correctly computed for message
        '''
        message = b"Test message"
        expected_md5 = hashlib.md5(message).hexdigest()
        
        address = ('0.0.0.0', 12345)
        result = self.data_processor.enrich_data(message, address)
        
        result_dict = json.loads(result)
        result_md5 = result_dict['md5_hash']
        
        self.assertEqual(result_md5, expected_md5)

    def test_data_format(self):
        '''
        Test that the returned data is in a valid JSON format
        '''
        message = b"Another test message"
        address = ('0.0.0.0', 54321)
        
        result = self.data_processor.enrich_data(message, address)
        
        try:
            result_dict = json.loads(result)
        except json.JSONDecodeError:
            self.fail("The result is not valid JSON.")
        
        self.assertIn('timestamp', result_dict)
        self.assertIn('client_ip', result_dict)
        self.assertIn('client_port', result_dict)
        self.assertIn('md5_hash', result_dict)
        self.assertIn('data', result_dict)

if __name__ == '__main__':
    unittest.main()
