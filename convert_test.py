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
        url_data = ['EUR', 'EUR', 10, '2019-10-11']
        response = self.client.get("/convert?src_currency={}&dest_currency={}&amount={}&date={}".format(*url_data))
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(bool(data), True)
        self.assertEqual(data['currency'], "EUR")
        self.assertEqual(data['amount'], 10)

    def test_convert_date(self):
        url_data = ['EUR', 'JPY', 80, '2018-10-11']
        response = self.client.get("/convert?src_currency={}&dest_currency={}&amount={}&date={}".format(*url_data))
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(bool(data), False)

    def test_convert_format(self):
        url_data = ['EUR', 'EUR', 10, '11-10-2019']
        response = self.client.get("/convert?src_currency={}&dest_currency={}&amount={}&date={}".format(*url_data))
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(bool(data), False)
    #
    def test_convert_curr(self):
        url_data = ['AUD', 'RON', 1, '2019-07-15']
        response = self.client.get("/convert?src_currency={}&dest_currency={}&amount={}&date={}".format(*url_data))
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(bool(data), True)
        self.assertEqual(data['currency'], "RON")
        self.assertEqual(data['amount'], 2.9541)

    def test_convert_curr2(self):
        url_data = ['BGN', 'NOK', 1, '2019-09-17']
        response = self.client.get("/convert?src_currency={}&dest_currency={}&amount={}&date={}".format(*url_data))
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(bool(data), True)
        self.assertEqual(data['currency'], "NOK")
        self.assertEqual(data['amount'], 5.0473)

    def test_convert_curr3(self):
        url_data = ['BGN', 'NOK', 894368950, '2019-09-17']
        response = self.client.get("/convert?src_currency={}&dest_currency={}&amount={}&date={}".format(*url_data))
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(bool(data), True)
        self.assertEqual(data['currency'], "NOK")
        self.assertEqual(data['amount'], 4514148401.335)

    def test_covert_form(self):
        response = self.client.post(
            '/', data={
                'src_currency': 'EUR',
                'dest_currency': 'EUR',
                'amount': 10,
                'date': '2019-10-11'
            }, follow_redirects=True)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(bool(data), True)
        self.assertEqual(data['currency'], "EUR")
        self.assertEqual(data['amount'], 10)


if __name__ == '__main__':
    unittest.main()
