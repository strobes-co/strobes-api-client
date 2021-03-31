from strobes_client.client import StrobesClient

s = StrobesClient("dev@wesecureapp.com", "a",
                  "qa1.strobes.wsa-apps.com", 80, "http")

resp = s.list_organizations()

print(resp.results)
print(resp.page)


for r in resp.results:
    print(r.id)
