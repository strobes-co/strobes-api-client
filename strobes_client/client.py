from typing import List, Dict, Union
from strobes_client.base_client import BaseClient
from strobes_client import resources
from strobes_client.helpers import check_status_code


class StrobesClient(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def list_organizations(self, page: int = 1) -> \
            resources.OrganizationListResource:
        r = self.s.get(f"{self.app_url}api/v1/organizations/?page={str(page)}")
        check_status_code(r)
        return resources.OrganizationListResource(r.json())

    def get_organization(self, org_id: str) -> resources.OrganizationResource:
        r = self.s.get(f"{self.app_url}api/v1/organizations/{org_id}/")
        check_status_code(r)
        return resources.OrganizationResource(r.json())

    def list_assets(self, org_id: str, page: int = 1, asset_type: List[int] =
                    []) -> resources.AssetListResource:
        if len(asset_type):
            qs = "&"
            for t in asset_type:
                qs += f"type[]={t}&"
            r = self.s.get(
                f"{self.app_url}api/v1/organizations/{org_id}/assets/?page="
                f"{str(page)}{qs}")
        else:
            r = self.s.get(
                f"{self.app_url}api/v1/organizations/{org_id}/assets/?page="
                f"{str(page)}")
        check_status_code(r)
        return resources.AssetListResource(r.json())

    def get_asset(self, org_id: str, asset_id: int) -> resources.AssetResource:
        r = self.s.get(
            f"{self.app_url}api/v1/organizations/{org_id}/assets/"
            f"{str(asset_id)}/")
        check_status_code(r)
        return resources.AssetResource(r.json())

    def create_asset(self, org_id: str) -> resources.AssetResource:
        pass

    def update_asset(self, org_id: str, asset_id: int, name: str = None,
                     exposed: int = None, mac_address: str = None,
                     hostname: str = None, sensitivity: int = None,
                     ipaddress: str = None) -> resources.AssetResource:
        patch_data: Dict[str, Union[str, int]] = {}
        r = self.s.get(
            f"{self.app_url}api/v1/organizations/{org_id}/assets/"
            f"{str(asset_id)}/")
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
            f"{self.app_url}api/v1/organizations/{org_id}/assets/"
            f"{str(asset_id)}/", json=patch_data)
        check_status_code(r)
        return resources.AssetResource(r.json())

    def list_vulnerabilities(self, org_id: str,
                             severity: List[int] = [1, 2, 3, 4, 5],
                             state: List[int] = [0, 1, 2, 3, 4, 5, 6, 7],
                             asset_type: List[int] = [1, 2, 3, 4],
                             assets: List[int] = [],
                             page: int = 1,
                             cve: str = "") -> resources.VulnerabilityListResource:
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
            f"{str(page)}{qs}")
        check_status_code(r)
        return resources.VulnerabilityListResource(r.json())

    def get_vulnerability(self, org_id: str, asset_id: int, vulnerability_id: int) -> resources.VulnerabilityResource:
        r = self.s.get(
            f"{self.app_url}api/v1/organizations/{org_id}/assets/{asset_id}/"
            f"bugs/{str(vulnerability_id)}/")
        check_status_code(r)

        return resources.VulnerabilityResource(r.json())

    def update_vulnerability(self, org_id: str, asset_id: int,
                             vulnerability_id: int, state: int = None,
                             severity: int = None, mitigation: str = None, steps_to_reproduce: str = None, title: str = None) \
            -> resources.VulnerabilityResource:
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
        r = self.s.patch(
            f"{self.app_url}api/v1/organizations/{org_id}/assets/{asset_id}/"
            f"bugs/{str(vulnerability_id)}/", json=patch_data)
        check_status_code(r)

        return resources.VulnerabilityResource(r.json())

    def search_cve(self, org_id: str, search_term: str) \
            -> resources.CVEListResource:
        r = self.s.get(
            f"{self.app_url}api/v1/organizations/{org_id}/cve/?q="
            f"{search_term}")
        check_status_code(r)

        return resources.CVEListResource(r.json())

    def update_vulnerability_tags(self, org_id: str, asset_id: int,
                                  vulnerability_id: int, bug_tags: List[str]) \
            -> resources.VulnerabilityResource:
        r1 = self.get_vulnerability(org_id, asset_id, vulnerability_id)
        for tag in r1.bug_tags:
            bug_tags.append(tag["name"])

        r2 = self.s.post(
            f"{self.app_url}api/v1/organizations/{org_id}/assets/{asset_id}/"
            f"bugs/{str(vulnerability_id)}/tags/", json={"tag_list": bug_tags})
        check_status_code(r2)
        return resources.VulnerabilityResource(r2.json())

    def get_scan_configs(self) -> resources.ScanConfigListResource:
        r = self.s.get(f"{self.app_url}api/v1/cicd/configurations/")
        check_status_code(r)
        return resources.ScanConfigListResource(r.json())

    def start_scan(self, config_id: int = None, config_name: str = None, target: str = None,
                   target_list: List[str] = None) -> resources.TaskResource:
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



    
