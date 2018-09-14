from gevent import monkey; monkey.patch_all()
import unittest
import os
import requests
from rest.rest import rest
from rest.ticker import ticker
from rest.utils import utils
from gevent.pool import Pool
import gevent


class FileTest(unittest.TestCase):
    filename = 'Little_Prince.docx'
    user_id = ""
    sign = ""
    desktop_id = ""
    CHECK_PROCESSING_TIME = 1
    POOL_SIZE = 20

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

        # query desktop
        _, resp = rest_api.desktop.get()
        cls.desktop_id = resp['result']['dataArr'][0]['matter_id']
        print("desktop_id={}".format(cls.desktop_id))

    def setUp(self):
        self.rest = rest()
        self.rest.headers['user-id'] = self.user_id
        self.rest.headers['sign'] = self.sign

    def test_upload_without_moveIn(self):
        self._test_upload(self.filename, None)
        pass

    def test_upload(self):
        self._test_upload(self.filename, self.desktop_id)
        pass

    def test_concurrent_upload(self):
        file_count = 10
        matters = []
        t = ticker()

        def upload_file(idx):
            nonlocal matters, t
            evt = gevent.event.Event()
            evt.clear()

            def callback(result):
                nonlocal matters, t, evt, idx
                t.lap("[{}] callback".format(idx))
                matters.append(result['result']['matter_id'])
                evt.set()

            t.lap("[{}] start".format(idx))
            t.lap()
            self._upload_file(self.filename, self.desktop_id, callback)
            t.lap()
            t.lap("[{}] uploaded".format(idx))
            evt.wait()

        pool = Pool(self.POOL_SIZE)
        indices = list(range(1, file_count+1))
        t.start()
        pool.map(upload_file, indices)

        t.print_verbose()
        for matter_id in matters:
            print("delete mater: {}".format(matter_id))
            resp = self._delete_matter(matter_id)
            self.assertTrue(resp['success'], resp.get('message', None))

    def _test_upload(self, filename, desktop_id):
        evt = gevent.event.Event()
        evt.clear()
        resp = None

        def callback(result):
            nonlocal resp, evt
            resp = result
            evt.set()

        self._upload_file(filename, desktop_id, callback)

        # wait for callback is returned
        evt.wait()

        self.assertIsNotNone(resp)
        self.assertTrue(resp['success'])
        self.assertFalse(resp['result']['is_processing'])

        matter_id = resp['result']['matter_id']

        # delete matter
        resp = self._delete_matter(matter_id)
        self.assertTrue(resp['success'], resp.get('message', None))

    def _delete_matter(self, matter_id):
        status, resp = self.rest.card.delete.get(matter_id)
        self._check_status_code(status)
        if not resp['success']:
            return resp

        status, resp = self.rest.card.drop.get(matter_id)
        self._check_status_code(status)
        return resp

    def _upload_file(self, filename, parent, callback=None):
        # Read file as binary data
        with open(filename, 'rb') as f:
            data = f.read()

        self.rest.headers['Content-Type'] = 'application/octet-stream'
        status, resp = self.rest.file.upload.post(params={
            'fileName': os.path.basename(self.filename),
            'fileSize': len(data),
            'moveIn': parent
        }, data=data)
        utils.check_status_code(status)

        self.rest.headers['Content-Type'] = 'application/json; charset=utf-8'
        if resp['success']:
            matter_id = resp['result']['matter_id']
            gevent.spawn_later(self.CHECK_PROCESSING_TIME, self._wait_matter_completed, matter_id, callback)
            return
        if callback:
            callback(resp)

    def _wait_matter_completed(self, matter_id, callback):
        status, resp = self.rest.card.get(matter_id)
        utils.check_status_code(status)
        if resp['success'] and resp['result']['is_processing']:
            gevent.spawn_later(self.CHECK_PROCESSING_TIME, self._wait_matter_completed, matter_id, callback)
            return
        if callback:
            callback(resp)


