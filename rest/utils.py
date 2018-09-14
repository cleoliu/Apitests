import requests

class utils:
    @staticmethod
    def check_status_code(status):
        if status != requests.codes.ok:
            raise Exception("HTTP status returned: {}".format(status))

    @staticmethod
    def pack_return_values(resp):
        success = resp.get('success', False)
        if success:
            return success, resp['result']
        return success, resp['message']