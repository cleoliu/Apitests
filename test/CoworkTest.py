import unittest
import os
import requests
import string
import random
from rest.rest import rest
from rest.utils import utils
from rest.cowork import Cowork
from rest.im_service import IMServicice

class CoworkTest(unittest.TestCase):
    user_id = ""
    sign = ""
    RANDOM_STRING_LEN = 8

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
        self.cowork_id = None

    def tearDown(self):
        if self.cowork_id:
            Cowork.delete(self.rest, self.cowork_id)

    def test_cowork(self):
        # create cowork
        title = 'cowork_test_title'
        success, result = Cowork.create(self.rest, title)
        self.assertTrue(success, result)
        self.assertEqual(result['mime_type'], 'u3d.matter.dock')
        self.assertEqual(result['content_type'], 'work')
        self.assertEqual(result['title'], title)
        self.assertIsNotNone(result.get('matter_id', None))

        # get cowork
        self.cowork_id = result['matter_id']
        print("cowork {} created".format(self.cowork_id))
        success, result = Cowork.get(self.rest, self.cowork_id)
        self.assertTrue(success, result)
        self.assertEqual(result['mime_type'], 'u3d.matter.dock')
        self.assertEqual(result['content_type'], 'work')
        self.assertEqual(result['title'], title)

        # delete cowork
        success, result = Cowork.delete(self.rest, self.cowork_id)
        self.assertTrue(success, result)
        print("cowork {} deleted".format(self.cowork_id))
        self.assertEqual(result['numberAffected'], 1)
        self.cowork_id = None
