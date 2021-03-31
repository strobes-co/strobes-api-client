# from strobes_client import enums
# from strobes_client.exceptions import ResourceException
from strobes_client.helpers import check_keys


class OrganizationResource:
    id: int = 0
    name: str = ""

    def __init__(self, data):
        keys = ["id", "name"]
        check_keys(data, keys)
        to_deserialize = {}
        for k in keys:
            to_deserialize[k] = data[k]
        self.__dict__ = to_deserialize


class OrganizationListResource:
    results: list = []
    page: int = 0

    def __init__(self, data):
        keys = ["results"]
        to_deserialize = {}
        check_keys(data, keys)
        to_deserialize["page"] = 1
        to_deserialize["results"] = []
        for org in data["results"]:
            to_deserialize["results"].append(OrganizationResource(org))
        self.__dict__ = to_deserialize
