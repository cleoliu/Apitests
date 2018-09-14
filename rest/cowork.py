from rest.utils import utils

class Cowork:
    @staticmethod
    def create(rest, title):
        data = {
            "title": title
        }
        print(rest.headers)
        status, resp = rest.work.create.post(json=data)
        utils.check_status_code(status)
        return utils.pack_return_values(resp)

    @staticmethod
    def get(rest, matter_id):
        status, resp = rest.work.get(id=matter_id)
        utils.check_status_code(status)
        return utils.pack_return_values(resp)

    @staticmethod
    def delete(rest, matter_id):
        status, resp = rest.work.delete.get(id=matter_id)
        utils.check_status_code(status)
        return utils.pack_return_values(resp)
