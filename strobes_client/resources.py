from typing import List, Union
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
                if k in response_data:
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
        to_deserialize["data"] = AssetInfoResource(
            response_data["data"], is_check_keys=False)

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
        to_deserialize["count"] = response_data["count"]
        self.__dict__ = to_deserialize


class VulnerabilityExtraInfoResource:
    os: str = ""
    port: int = -1
    cpe: str = ""

    def __init__(self, response_data={}, is_check_keys=False):
        keys = ["os", "port", "cpe"]
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
    scanner_raw_response: dict = {}
    asset: Union[int, AssetResource] = -1

    def __init__(self, response_data={}, is_check_keys=False):
        keys = ["id", "title", "description", "steps_to_reproduce",
                "state", "exploit_available", "patch_available", "cwe", "cvss",
                "cve", "severity", "reported_by", "due_date", "asset"]
        to_deserialize = {}

        if is_check_keys:
            check_keys(response_data, keys)
        if type(response_data.get("asset")) != int:
            response_data["asset"] = response_data["asset"]["id"]
        for k in keys:
            to_deserialize[k] = response_data[k]
        self.__dict__ = to_deserialize


class VulnerabilityListResource:
    results: List[VulnerabilityResource] = []
    count: int = -1

    def __init__(self, response_data={}, is_check_keys=False):
        keys = ["results", "count"]
        to_deserialize = {}
        if is_check_keys:
            check_keys(response_data, keys)
        to_deserialize["results"] = []
        for v in response_data["results"]:
            to_deserialize["results"].append(VulnerabilityResource(v))
        to_deserialize["count"] = response_data["count"]
        self.__dict__ = to_deserialize


class CVEResource:
    id: int = -1
    cve_id: str = ""
    cvss: float = -1

    def __init__(self, response_data={}, is_check_keys=False):
        keys = ["id", "cve_id", "cvss"]
        to_deserialize = {}
        for k in keys:
            to_deserialize[k] = response_data[k]
        self.__dict__ = to_deserialize


class CVEListResource:
    results: List[CVEResource] = []
    count: int = -1

    def __init__(self, response_data={}, is_check_keys=False):
        keys = ["results", "count"]
        to_deserialize = {}
        if is_check_keys:
            check_keys(response_data, keys)
        to_deserialize["results"] = []
        for cve in response_data["results"]:
            to_deserialize["results"].append(CVEResource(cve))
        to_deserialize["count"] = response_data["count"]
        self.__dict__ = to_deserialize
