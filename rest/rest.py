import requests
import json as JSON

class rest:
    API_PREFIX = 'uHutt'
    endpoint = '127.0.0.1'
    port = 9966
    is_https = False

    methods = {
        "get": None,
        "post": None,
        "put": None,
        "del": None
    }

    headers = {'Content-Type': 'application/json'}

    def __init__(self):
        self.methods["get"] = self._get
        self.methods["post"] = self._post
        self.methods["put"] = self._put
        self.methods["del"] = self._delete

        self.path = ''
        self.url = ''

    def __getattr__(self, item):
        if item not in self.methods.keys():
            self.path += "{}/".format(item)
            return self
        # remove the last '/' character
        self.url = rest._get_base_url() + self.path[:-1]
        self.path = ''
        return  self.methods[item]

    def _get(self, id=None, params=None):
        url = "{}/{}".format(self.url, id) if id else self.url
        print("GET {}, params={}".format(url, params))
        resp = requests.get(url=url, headers=self.headers, params=params)
        return rest._pack_response(resp)

    def _post(self, params=None, json=None, data=None):
        print("POST {}, params={}".format(self.url, params))
        resp = requests.post(url=self.url, headers=self.headers, params=params, json=json) if json else \
               requests.post(url=self.url, headers=self.headers, params=params, data=data)
        return rest._pack_response(resp)

    def _put(self, params=None, json=None, data=None):
        print("PUT {}, params={}".format(self.url, params))
        resp = requests.put(url=self.url, headers=self.headers, params=params, json=json) if json else \
               requests.put(url=self.url, headers=self.headers, params=params, data=data)
        return rest._pack_response(resp)

    def _delete(self, id, params=None):
        url = "{}/{}".format(self.url, id)
        print("DELETE {}, params={}".format(url, params))
        resp = requests.delete(url=url, headers=self.headers, params=params)
        return rest._pack_response(resp)

    @staticmethod
    def _pack_response(resp):
        try:
            resp_json = JSON.loads(resp.text)
            if resp_json['success']:
                return resp.status_code, resp_json

            return resp.status_code, {
                'success': False,
                'message': rest._compose_error_message(resp_json)
            }
        except ValueError as err:
            return resp.status_code, {
                'success': False,
                'message': "Unable to parse to JSON format: {}".format(resp.text)
            }
        except Exception as e:
            return resp.status_code, {
                'success': False,
                'message': "Unexpected error: {}".format(e)
            }

    @staticmethod
    def _get_base_url():
        return "{}://{}:{}/{}/".format('https' if rest.is_https else 'http',
                                       rest.endpoint,
                                       rest.port,
                                       rest.API_PREFIX)

    @staticmethod
    def _compose_error_message(resp_json):
        return "{}({}): {}".format(resp_json['errorType'], resp_json['errorCode'], resp_json['message'])