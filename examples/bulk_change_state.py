'''
This example shows how to filter vulnerabilities in an organization by CVE 
and update their state to patched
'''

from strobes_client.client import StrobesClient

s = StrobesClient(email="dev@wesecureapp.com", password="a",
                  host="qa1.strobes.wsa-apps.com", port=80, scheme="http")


# Define organization ID

organization_id = "802caa9a-ece9-4dfb-8b18-e2154319d3f5"

'''
Get list of vulnerabilities
'''

for p in range(1, 10):  # page 1 to 10
    vulnerabilities = s.list_vulnerabilities(
        org_id=organization_id, page=p, cve="CVE-2020-0909")
    for v in vulnerabilities.results:
        updated_vulnerability = s.update_vulnerability(
            org_id=organization_id, asset_id=v.asset, vulnerability_id=v.id, state=2)
        print(updated_vulnerability.state)
