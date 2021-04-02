from typing import List, Dict, Union
from strobes_client.base_client import BaseClient
from strobes_client import resources


class StrobesClient(BaseClient):
    def __init__(self, *args):
        super().__init__(*args)

    def list_organizations(self, page: int = 1) -> \
            resources.OrganizationListResource:
        r = self.s.get(f"{self.app_url}api/v1/organizations/?page={str(page)}")
        return resources.OrganizationListResource(r.json())

    def get_organization(self, org_id: str) -> resources.OrganizationResource:
        r = self.s.get(f"{self.app_url}api/v1/organizations/{org_id}/")
        return resources.OrganizationResource(r.json())

    def get_assets(self, org_id: str, page: int = 1, asset_type: List[int] =
                   []) -> resources.AssetListResource:
        if len(asset_type):
            qs = "&"
            for t in asset_type:
                qs += f"type[]={t}&"
            r = self.s.get(
                f"{self.app_url}api/v1/organizations/{org_id}/assets/?page="
                f"{page}{qs}")
        else:
            r = self.s.get(
                f"{self.app_url}api/v1/organizations/{org_id}/assets/?page="
                f"{page}")
        return resources.AssetListResource(r.json())

    def get_asset(self, org_id: str, asset_id: int) -> resources.AssetResource:
        r = self.s.get(
            f"{self.app_url}api/v1/organizations/{org_id}/assets/"
            f"{str(asset_id)}/")
        return resources.AssetResource(r.json())

    def update_asset(self, org_id: str, asset_id: int, name: str = None,
                     exposed: int = None, mac_address: str = None,
                     hostname: str = None, sensitivity: int = None,
                     ipaddress: str = None) -> resources.AssetResource:
        patch_data: Dict[str, Union[str, int]] = {}
        r = self.s.get(
            f"{self.app_url}api/v1/organizations/{org_id}/assets/"
            f"{str(asset_id)}/")
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
        return resources.AssetResource(r.json())
