from typing import List
# from strobes_client import enums
# from strobes_client.exceptions import ResourceException
from strobes_client.helpers import check_keys


class OrganizationResource:
    id: int = -1
    name: str = ""

    def __init__(self, response_data):
        keys = ["id", "name"]
        check_keys(response_data, keys)
        to_deserialize = {}
        for k in keys:
            to_deserialize[k] = response_data[k]
        self.__dict__ = to_deserialize


class OrganizationListResource:
    results: list = []
    page: int = -1

    def __init__(self, response_data):
        keys = ["results"]
        to_deserialize = {}
        check_keys(response_data, keys)
        to_deserialize["page"] = 1
        to_deserialize["results"] = []
        for org in response_data["results"]:
            to_deserialize["results"].append(OrganizationResource(org))
        self.__dict__ = to_deserialize


class AssetInfoResource:
    os: str = ""
    cpe: str = ""
    netbios: str = ""
    hostname: str = ""
    ipaddress: str = ""
    mac_address: str = ""

    def __init__(self, response_data):
        keys = ["os", "cpe", "netbios", "hostname", "ipaddress", "mac_address"]
        to_deserialize = {}
        if response_data:
            check_keys(response_data, keys)
            for k in keys:
                to_deserialize[k] = response_data[k]
            self.__dict__ = to_deserialize


class AssetResource:
    id: int = -1
    name: str = ""
    organization: str = ""
    sensitivity: int = -1
    exposed: int = -1
    target: str = ""
    type: int = -1
    cloud_type: int = -1
    linked_assets: List[int] = []
    data: AssetInfoResource = AssetInfoResource(
        {"os": "", "cpe": "", "netbios": "", "hostname": "", "ipaddress": "",
         "mac_address": ""})

    def __init__(self, response_data):
        keys = ["id", "name", "organization", "sensitivity",
                "exposed", "target", "cloud_type", "type", "linked_assets",
                "data"]
        to_deserialize = {}
        check_keys(response_data, keys)
        to_deserialize["data"] = AssetInfoResource(response_data["data"])

        del response_data["data"]
        keys.remove('data')
        for k in keys:
            to_deserialize[k] = response_data[k]
        self.__dict__ = to_deserialize


class AssetListResource:
    results: list = []
    page: int = 0

    def __init__(self, response_data):
        keys = ["results"]
        to_deserialize = {}
        check_keys(response_data, keys)
        to_deserialize["page"] = 1
        to_deserialize["results"] = []
        for asset in response_data["results"]:
            to_deserialize["results"].append(AssetResource(asset))
        self.__dict__ = to_deserialize
