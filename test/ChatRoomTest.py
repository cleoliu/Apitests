import unittest
import requests
import json
from rest.rest import rest
from rest.im_service import IMServicice

class ChatRoomTest(unittest.TestCase):
    user_id = ""
    sign = ""

    @classmethod
    def setUpClass(cls):
        user = "cleo@mailinator.com"
        password = "123123"

        # login
        rest_api = rest()
        _, resp = rest_api.account.connect.post(json={
            "email": user, "password": password, "ccap": "captcha"
        })
        cls.user_id = resp['result']['user_id']
        cls.sign = resp['result']['sign']
        rest_api.headers['user-id'] = cls.user_id
        rest_api.headers['sign'] = cls.sign
        print("user_id={}".format(cls.user_id))
        print("sign={}".format(cls.sign))

    def setUp(self):
        self.rest = rest()
        self.rest.headers['user-id'] = self.user_id
        self.rest.headers['sign'] = self.sign

    def test_send_msg(self):
        im = IMServicice()
        params = {
            "id": self.user_id,
            "name": 'kurt',
            "sign": self.sign
        }
        resp = im.create_user(params)
        self.assertTrue(resp['success'], resp.get('message', None))

        resp = im.delete_user(params)
        self.assertTrue(resp['success'], resp.get('message', None))
