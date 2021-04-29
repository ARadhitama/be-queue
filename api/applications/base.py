class Application:
    def get_data_list_dict_by_key(self, list_dict: list, key: str, value) -> dict or None:
        for data in list_dict:
            if data[key] == value:
                return data
        return None


class BaseError(Exception):
    def __init__(self, message):
        self.message = message