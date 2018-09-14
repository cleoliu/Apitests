import requests


class IMServicice:
    host = '127.0.0.1'
    USER_SERVICE_PATH = "userService/userservice"
    USER_SERVICE_SECRET = "0k1sGHSv"
    REST_API_PATH = "restapi/v1"
    REST_API_KEY = "8fNCNCCrdWO931Hw"

    def create_user(self, params):
        return self._send_user_request('add', params)

    def delete_user(self, params):
        return self._send_user_request('delete', params)

    def _send_user_request(self, action, params):
        url = "{}/{}".format(self._get_base_url(), self.USER_SERVICE_PATH)
        params = {
            "type": action,
            "secret": self.USER_SERVICE_SECRET,
            "username": params['id'],
            "password": params['sign'],
            "name": params['name']
        }
        resp = requests.get(url, params=params)
        if resp.status_code == requests.codes.ok and \
           resp.text == '<result>ok</result>\n':
            return {
                'success': True
            }
        return {
            'success': False,
            'message': "status: {}, text: {}".format(resp.status_code, resp.text)
        }

    @staticmethod
    def _get_base_url():
        return "http://{}:9090/plugins".format(IMServicice.host)