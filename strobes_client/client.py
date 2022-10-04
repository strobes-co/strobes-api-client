from typing import List, Dict, Union

import requests
from strobes_client.base_client import BaseClient
from strobes_client import resources
from strobes_client.helpers import check_status_code
from strobes_client.enums import VulnerabilityTypeEnum, AssetTypeEnum


class StrobesClient(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def list_organizations(self, page: int = 1) -> resources.OrganizationListResource:
        r = self.s.get(f"{self.app_url}api/v1/organizations/?page={str(page)}")
        check_status_code(r)
        return resources.OrganizationListResource(r.json())

    def get_organization(self, org_id: str) -> resources.OrganizationResource:
        r = self.s.get(f"{self.app_url}api/v1/organizations/{org_id}/")
        check_status_code(r)
        return resources.OrganizationResource(r.json())

    def list_assets(
        self, org_id: str, page: int = 1, asset_type: List[int] = []
    ) -> resources.AssetListResource:
        if len(asset_type):
            qs = "&"
            for t in asset_type:
                qs += f"type[]={t}&"
            r = self.s.get(
                f"{self.app_url}api/v1/organizations/{org_id}/assets/?page="
                f"{str(page)}{qs}"
            )
        else:
            r = self.s.get(
                f"{self.app_url}api/v1/organizations/{org_id}/assets/?page="
                f"{str(page)}"
            )
        check_status_code(r)
        return resources.AssetListResource(r.json())

    def get_asset(self, org_id: str, asset_id: int) -> resources.AssetResource:
        r = self.s.get(
            f"{self.app_url}api/v1/organizations/{org_id}/assets/{asset_id}/"
        )
        check_status_code(r)
        return resources.AssetResource(r.json())

    def create_asset(
        self,
        org_id: str,
        name: str,
        exposed: int,
        sensitivity: int,
        target: str,
        asset_type: str,
        **kwargs,
    ) -> resources.AssetResource:
        post_data: Dict[str, Union[str, int]] = {
            "name": name,
            "sensitivity": sensitivity,
            "exposed": exposed,
            "target": target,
            "tags": kwargs.get("asset_tags", []),
            "linked_assets": kwargs.get("linked_assets", []),
            "invite": kwargs.get("invite", []),
            "add_users": kwargs.get("add_users", []),
        }

        if asset_type == AssetTypeEnum.web.value:
            post_data["type"] = AssetTypeEnum.web_asset_level.value

        if asset_type == AssetTypeEnum.mobile.value:
            post_data["type"] = AssetTypeEnum.mobile_asset_level.value

        if asset_type == AssetTypeEnum.network.value:
            post_data["type"] = AssetTypeEnum.network_asset_level.value
            if kwargs.get("target_list", []):
                post_data["subnet"] = True
                post_data["name"] = ""
                post_data["target"] = ""
                post_data["target_list"] = kwargs.get("target_list", [])
                post_data["exclude_ip_list"] = kwargs.get("exclude_ip_list", [])
            else:
                post_data["data"] = {}
                post_data["data"]["mac_address"] = kwargs.get("mac_address", "")
                post_data["data"]["os"] = kwargs.get("os", "")
                post_data["data"]["hostname"] = kwargs.get("hostname", "")
                post_data["data"]["cpe"] = kwargs.get("cpe", "")

        if asset_type == AssetTypeEnum.cloud.value:
            post_data["type"] = AssetTypeEnum.cloud_asset_level.value
            post_data["cloud_type"] = kwargs.get("cloud_type", 1)

        r = self.s.post(
            f"{self.app_url}api/v2/organizations/{org_id}/assets/",
            json=post_data,
        )

        check_status_code(r)
        return resources.AssetResource(r.json())

    def update_asset(
        self,
        org_id: str,
        asset_id: int,
        name: str = None,
        exposed: int = None,
        mac_address: str = None,
        hostname: str = None,
        sensitivity: int = None,
        ipaddress: str = None,
    ) -> resources.AssetResource:
        patch_data: Dict[str, Union[str, int]] = {}
        r = self.s.get(
            f"{self.app_url}api/v1/organizations/{org_id}/assets/{asset_id}/"
        )
        check_status_code(r)
        asset_data = resources.AssetResource(r.json())
        if name:
            patch_data["name"] = name
        else:
            patch_data["name"] = asset_data.name
        if exposed:
            patch_data["exposed"] = exposed
        else:
            patch_data["exposed"] = asset_data.exposed
        if mac_address:
            patch_data["mac_address"] = mac_address
        else:
            patch_data["mac_address"] = asset_data.data.mac_address
        if hostname:
            patch_data["hostname"] = hostname
        else:
            patch_data["hostname"] = asset_data.data.hostname

        if sensitivity:
            patch_data["sensitivity"] = sensitivity
        else:
            patch_data["sensitivity"] = asset_data.sensitivity
        if ipaddress:
            patch_data["ipaddress"] = ipaddress
        else:
            patch_data["ipaddress"] = asset_data.data.ipaddress

        r = self.s.patch(
            f"{self.app_url}api/v1/organizations/{org_id}/assets/{asset_id}/",
            json=patch_data,
        )
        check_status_code(r)
        return resources.AssetResource(r.json())

    def list_vulnerabilities(
        self,
        org_id: str,
        severity: List[int] = [1, 2, 3, 4, 5],
        state: List[int] = [0, 1, 2, 3, 4, 5, 6, 7],
        asset_type: List[int] = [1, 2, 3, 4],
        assets: List[int] = [],
        page: int = 1,
        cve: str = "",
    ) -> resources.VulnerabilityListResource:
        qs = "&"
        if len(asset_type):
            qs += "filter_by[]=asset_type&"
            for at in asset_type:
                qs += f"asset_type[]={str(at)}&"
        if len(state):
            qs += "filter_by[]=state&"
            for st in state:
                qs += f"state[]={str(st)}&"
        if len(assets):
            qs += "filter_by[]=assets&"
            for a in assets:
                qs += f"assets[]={str(a)}&"
        if len(severity):
            qs += "filter_by[]=severity&"
            for sv in severity:
                qs += f"severity[]={str(sv)}&"
        if cve:
            qs += "filter_by[]=cve&"
            cve_data = self.search_cve(org_id, cve).results
            if len(cve_data) > 0:
                cve_id = cve_data[0].id
                qs += f"cve[]={str(cve_id)}"
        r = self.s.get(
            f"{self.app_url}api/v1/organizations/{org_id}/bugs/?page="
            f"{str(page)}{qs}"
        )
        check_status_code(r)
        return resources.VulnerabilityListResource(r.json())

    def get_vulnerability(
        self, org_id: str, asset_id: int, vulnerability_id: int
    ) -> resources.VulnerabilityResource:
        r = self.s.get(
            f"{self.app_url}api/v1/organizations/{org_id}/assets/{asset_id}/"
            f"bugs/{str(vulnerability_id)}/"
        )
        check_status_code(r)

        return resources.VulnerabilityResource(r.json())

    def update_vulnerability(
        self,
        org_id: str,
        asset_id: int,
        vulnerability_id: int,
        state: int = None,
        severity: int = None,
        mitigation: str = None,
        steps_to_reproduce: str = None,
        title: str = None,
        vulnerable_id: str = None,
        aws_category: str = None,
        region: str = None,
    ) -> resources.VulnerabilityResource:
        patch_data: Dict[str, Union[str, int]] = {}
        if state:
            patch_data["state"] = state
        if severity:
            patch_data["severity"] = severity
        if mitigation:
            patch_data["mitigation"] = mitigation
        if steps_to_reproduce:
            patch_data["steps_to_reproduce"] = steps_to_reproduce
        if title:
            patch_data["title"] = title
        if vulnerable_id or aws_category or region:
            patch_data["cloud"] = {}
            if vulnerable_id:
                patch_data["cloud"]["vulnerable_id"] = vulnerable_id
            if aws_category:
                patch_data["cloud"]["aws_category"] = aws_category
            if region:
                patch_data["cloud"]["region"] = region
        r = self.s.patch(
            f"{self.app_url}api/v1/organizations/{org_id}/assets/{asset_id}/"
            f"bugs/{str(vulnerability_id)}/",
            json=patch_data,
        )
        check_status_code(r)
        return resources.VulnerabilityResource(r.json())

    def search_cve(self, org_id: str, search_term: str) -> resources.CVEListResource:
        r = self.s.get(
            f"{self.app_url}api/v1/organizations/{org_id}/cve/?q={search_term}"
        )
        check_status_code(r)

        return resources.CVEListResource(r.json())

    def update_vulnerability_tags(
        self, org_id: str, asset_id: int, vulnerability_id: int, bug_tags: List[str]
    ) -> resources.VulnerabilityResource:
        r1 = self.get_vulnerability(org_id, asset_id, vulnerability_id)
        for tag in r1.bug_tags:
            bug_tags.append(tag["name"])

        r2 = self.s.post(
            f"{self.app_url}api/v1/organizations/{org_id}/assets/{asset_id}/"
            f"bugs/{str(vulnerability_id)}/tags/",
            json={"tag_list": bug_tags},
        )
        check_status_code(r2)
        return resources.VulnerabilityResource(r2.json())

    def get_scan_configs(self) -> resources.ScanConfigListResource:
        r = self.s.get(f"{self.app_url}api/v1/cicd/configurations/")
        check_status_code(r)
        return resources.ScanConfigListResource(r.json())

    def start_scan(
        self,
        config_id: int = None,
        config_name: str = None,
        target: str = None,
        target_list: List[str] = None,
    ) -> resources.TaskResource:
        data = {}
        if config_id:
            data["configuration_id"] = config_id
        else:
            data["configuration_name"] = config_name
        if target:
            data["target"] = target
        if target_list:
            data["target_list"] = target_list

        r = self.s.post(f"{self.app_url}api/v1/cicd/scan/", json=data)
        check_status_code(r)
        return resources.TaskResource(r.json())

    def get_scan_status(self, task_id: str) -> resources.TaskResource:
        r = self.s.get(f"{self.app_url}api/v1/cicd/status/{task_id}/")
        check_status_code(r)
        return resources.TaskResource(r.json())

    def create_vulnerability(
        self,
        org_id: str,
        asset_id: int,
        vulnerability_type: str,
        title: str,
        description: str,
        mitigation: str,
        steps_to_reproduce: str,
        severity: int,
        **kwargs,
    ) -> resources.VulnerabilityResource:
        post_data: Dict[str, Union[str, int]] = {}

        post_data["title"] = title
        post_data["description"] = description
        post_data["mitigation"] = mitigation
        post_data["steps_to_reproduce"] = steps_to_reproduce
        post_data["severity"] = severity
        post_data["cve_list"] = kwargs.get("cve_list", [])
        post_data["cwe_list"] = kwargs.get("cwe_list", [])

        if vulnerability_type == VulnerabilityTypeEnum.code.value:
            post_data["bug_level"] = VulnerabilityTypeEnum.code_bug_level.value
            post_data["code"] = {}
            post_data["code"]["vulnerable_code"] = kwargs.get("vulnerable_code", None)
            post_data["code"]["start_line_number"] = kwargs.get(
                "start_line_number", None
            )
            post_data["code"]["column_number"] = kwargs.get("column_number", None)
            post_data["code"]["file_name"] = kwargs.get("file_name", None)
            post_data["code"]["end_line_number"] = kwargs.get("end_line_number", None)
            post_data["code"]["end_column"] = kwargs.get("end_column", None)

        if vulnerability_type == VulnerabilityTypeEnum.web.value:
            post_data["bug_level"] = VulnerabilityTypeEnum.web_bug_level.value
            post_data["web"] = {}
            post_data["web"]["request"] = kwargs.get("request", None)
            post_data["web"]["response"] = kwargs.get("response", None)
            post_data["web"]["affected_endpoints"] = kwargs.get(
                "affected_endpoints", []
            )

        if vulnerability_type == VulnerabilityTypeEnum.network.value:
            post_data["bug_level"] = VulnerabilityTypeEnum.network_bug_level.value
            post_data["network"] = {}
            post_data["network"]["port_address"] = kwargs.get("port_address", None)
            post_data["network"]["cpe"] = kwargs.get("cpe", None)
            post_data["network"]["os"] = kwargs.get("os", None)

        if vulnerability_type == VulnerabilityTypeEnum.cloud.value:
            post_data["bug_level"] = VulnerabilityTypeEnum.cloud_bug_level.value
            post_data["cloud"] = {}
            post_data["cloud"]["region"] = kwargs.get("region", None)
            post_data["cloud"]["vulnerable_id"] = kwargs.get("vulnerable_id", None)
            post_data["cloud"]["aws_category"] = kwargs.get("aws_category", None)

        if vulnerability_type == VulnerabilityTypeEnum.package.value:
            post_data["bug_level"] = VulnerabilityTypeEnum.package_bug_level.value
            post_data["package"] = {}
            post_data["package"]["installed_version"] = kwargs.get(
                "installed_version", None
            )
            post_data["package"]["fixed_version"] = kwargs.get("fixed_version", None)
            post_data["package"]["package_name"] = kwargs.get("package_name", None)
            post_data["package"]["affected_versions"] = kwargs.get(
                "affected_versions", None
            )

        r = self.s.post(
            f"{self.app_url}api/v1/organizations/{org_id}/assets/{asset_id}/bugs/",
            json=post_data,
        )
        check_status_code(r)
        return resources.VulnerabilityResource(r.json())
