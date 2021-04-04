from typing import List
# from strobes_client import enums
# from strobes_client.exceptions import ResourceException
from strobes_client.helpers import check_keys


class OrganizationResource:
    id: int = -1
    name: str = ""

    def __init__(self, response_data={}, is_check_keys=False):
        keys = ["id", "name"]
        if is_check_keys:
            check_keys(response_data, keys)
        to_deserialize = {}
        for k in keys:
            to_deserialize[k] = response_data[k]
        self.__dict__ = to_deserialize


class OrganizationListResource:
    results: list = []
    count: int = -1

    def __init__(self, response_data={}, is_check_keys=False):
        keys = ["results", "count"]
        to_deserialize = {}
        if is_check_keys:
            check_keys(response_data, keys)
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

    def __init__(self, response_data={}, is_check_keys=False):
        keys = ["os", "cpe", "netbios", "hostname", "ipaddress", "mac_address"]
        to_deserialize = {}
        if response_data:
            if is_check_keys:
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
    data: AssetInfoResource = AssetInfoResource()

    def __init__(self, response_data={}, is_check_keys=False):
        keys = ["id", "name", "organization", "sensitivity",
                "exposed", "target", "cloud_type", "type", "linked_assets",
                "data"]
        to_deserialize = {}
        if is_check_keys:
            check_keys(response_data, keys)
        to_deserialize["data"] = AssetInfoResource(response_data["data"])

        del response_data["data"]
        keys.remove('data')
        for k in keys:
            to_deserialize[k] = response_data[k]
        self.__dict__ = to_deserialize


class AssetListResource:
    results: List[AssetResource] = []
    count: int = -1

    def __init__(self, response_data={}, is_check_keys=False):
        keys = ["results", "count"]
        to_deserialize = {}
        if is_check_keys:
            check_keys(response_data, keys)
        to_deserialize["results"] = []
        for asset in response_data["results"]:
            to_deserialize["results"].append(AssetResource(asset))
        self.__dict__ = to_deserialize


class VulnerabilityExtraInfoResource:
    os: str = ""
    port: int = -1
    cpe: str = ""

    def __init__(self, response_data={}, is_check_keys=False):
        keys = ["os", "os", "port", "cpe"]
        to_deserialize = {}
        if response_data:
            if is_check_keys:
                check_keys(response_data, keys)
            for k in keys:
                to_deserialize[k] = response_data[k]
            self.__dict__ = to_deserialize


class VulnerabilityResource:
    id: int = -1
    title: str = ""
    description: str = ""
    steps_to_reproduce: str = ""
    state: int = -1
    exploit_available: bool = False
    patch_available: bool = False
    cwe: List[int] = []
    cvss: float = -1
    cve: List[str] = []
    severity: int = -1
    reported_by: str = ""
    due_date: str = ""
    extra_info: VulnerabilityExtraInfoResource = \
        VulnerabilityExtraInfoResource()

    def __init__(self, response_data={}, is_check_keys=False):
        keys = ["id", "title", "description", "steps_to_reproduce",
                "state", "exploit_available", "patch_available", "cwe", "cvss",
                "cve", "severity", "reported_by", "due_data"]
        to_deserialize = {}
        if is_check_keys:
            check_keys(response_data, keys)
        to_deserialize["results"] = []
        for asset in response_data["results"]:
            to_deserialize["results"].append(AssetResource(asset))
        self.__dict__ = to_deserialize


class VulnerabilityListResource:
    results: List[VulnerabilityResource] = []
    count: int = -1
