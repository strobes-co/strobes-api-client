from strobes_client.base_client import BaseClient
from strobes_client import resources


class StrobesClient(BaseClient):
    def __init__(self, *args):
        super().__init__(*args)

    def list_organizations(self, page: int = 1):
        r = self.s.get(f"{self.app_url}api/v1/organizations/?page={str(page)}")
        return resources.OrganizationListResource(r.json())
