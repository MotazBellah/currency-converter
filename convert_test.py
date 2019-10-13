from flask import current_app
from app import app
import unittest
import json

class AppTestCase(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        self.app = app
        app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    # executed after each test
    def tearDown(self):
        self.app_context.pop()

    def test_app_exists(self):
        """Test if the app exists """
        self.assertFalse(current_app is None)

    def test_home_page(self):
        """Test the home page"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_convert(self):
        response = self.app.get("/dummy")
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(data['dummy'], "dummy-value")

if __name__ == '__main__':
    unittest.main()
