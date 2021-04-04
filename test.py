from strobes_client.client import StrobesClient

s = StrobesClient("dev@wesecureapp.com", "a",
                  "qa1.strobes.wsa-apps.com", 80, "http")

# resp = s.list_organizations()
# print(resp.results)
# print(resp.results)
# print(resp.count)

# # print(dir(resp))
# for r in resp.results:
#     print(r.id)

# resp = s.get_organization(org_id="3971bd9f-4e59-4f94-b02d-3119cd8d609f")
# print(resp)

# resp = s.get_assets(
#     org_id="f1e2d7d5-45d7-4ded-8b76-f90358596901", asset_type=[1])
# print(resp.results)

# for r in resp.results:
#     print(r.data)

# resp = s.get_asset(
#     org_id="f1e2d7d5-45d7-4ded-8b76-f90358596901", asset_id=42)
# print(resp)

resp = s.update_asset(
    org_id="f1e2d7d5-45d7-4ded-8b76-f90358596901", asset_id=42, name="abc")
print(resp.name)


