'''
This example shows how to fetch assets in an organization 
and update their exposed flag to private
'''

from strobes_client.client import StrobesClient

s = StrobesClient("dev@wesecureapp.com", "a",
                  "qa1.strobes.wsa-apps.com", 80, "http")


# Define organization ID

organization_id = "802caa9a-ece9-4dfb-8b18-e2154319d3f5"

'''
Get list of assets
'''

for p in range(1, 10):  # page 1 to 10
    assets = s.list_assets(
        org_id=organization_id, page=p)
    for at in assets.results:
        updated_asset = s.update_asset(
            org_id=organization_id, asset_id=at.id,
            exposed=2)
        print(updated_asset.exposed)
