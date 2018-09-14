import unittest
import requests
import json
from rest.rest import rest

class AccountTest(unittest.TestCase):
    def setUp(self):
        self.payload = {
            "email": "cleo@mailinator.com",
            "password": "123123",
            "ccap": "captcha"
        }
        self.rest = rest()


    def test_connect1(self):
        url = 'http://127.0.0.1:9966/uHutt/account/connect'
        headers = {'Content-Type': 'application/json'}

        resp = requests.post(url=url, headers=headers, json=self.payload)
        self.assertEqual(resp.status_code, requests.codes.ok)
        resp_json = json.loads(resp.text)
        self.assertTrue(resp_json['success'])

    def test_connect2(self):
        status, resp = self.rest.account.connect.post(json=self.payload)
        self.assertEqual(status, requests.codes.ok)
        self.assertTrue(resp['success'], resp.get('message', None))

        self.payload['password'] = 'wrong'
        status, resp = self.rest.account.connect.post(json=self.payload)
        self.assertEqual(status, requests.codes.ok)
        self.assertFalse(resp['success'], resp.get('message', None))

    def __compose_error_message(self, resp_json):
        if not resp_json['success']:
            return "{}({}): {}".format(resp_json['errorType'],
                             resp_json['errorCode'],
                             resp_json['message'])

if __name__ == '__main__':
    unittest.main()