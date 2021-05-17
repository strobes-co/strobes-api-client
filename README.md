# :cyclone: Strobes API Client
Strobes API client is an API wrapper written in python that helps you to integrate Strobes with you existing tooling. 

# Current Version
```
v0.1
```

# :mortar_board: Using the client

- Install the client
```
python setup.py install
```
- Import the client

```
from strobes_client.client import StrobesClient
```

- Initialize the client

```
s = StrobesClient("email@example.com", "yourpassword", qa1.strobes.wsa-apps.com", 80, "http")
```

- Example call

```
resp = s.list_organizations()
resp.results

[<strobes_client.resources.OrganizationResource object at 0x109aee400>, <strobes_client.resources.OrganizationResource object at 0x109aee3a0>, <strobes_client.resources.OrganizationResource object at 0x109b240a0>, <strobes_client.resources.OrganizationResource object at 0x109b240d0>]
```

# :wrench: APIs

### list_organizations

**Expected**

| Name  | Required | Default | Description |
| ------------- | ------------- | ------------- | ------------- |
| page  | No  | 1 | The page number for organization list|

**Returns**

```
List[OrganizationResource]
```


### get_organization

**Expected**

| Name  | Required | Default | Description |
| ------------- | ------------- | ------------- | ------------- |
| org_id  | Yes  | | The organization UUID |

**Returns**

```
OrganizationResource
```

### get_assets

**Expected**

| Name  | Required | Default | Description |
| ------------- | ------------- | ------------- | ------------- |
| org_id  | Yes  | | The organization UUID |
| page  | No  |1 | The page number for asset list |
| asset_type  | No  |[] | The type of assets you want to filter by. For example, asset_type=[1,2]  |

**Returns**

```
List[AssetResource]
```

### get_asset

**Expected**

| Name  | Required | Default | Description |
| ------------- | ------------- | ------------- | ------------- |
| org_id  | Yes  | | The organization UUID |
| asset_id  | Yes  || The asset ID |

**Returns**

```
AssetResource
```

### update_asset

**Expected**

| Name  | Required | Default | Description |
| ------------- | ------------- | ------------- | ------------- |
| org_id  | Yes  | | The organization UUID |
| asset_id  | Yes  || The asset ID |
| name  | No  || The asset name |
| mac_address  | No  || The mac_address of the asset |
| hostname  | No  || The hostname of the asset  |
| ipaddress  | No  || The ipaddress of the asset  |
| sensitivity  | No  || The business sensitivity of the asset  |
| exposure  | No  || The exposure of the asset  |

**Returns**

```
AssetResource
```

### list_vulnerabilities

**Expected**

| Name  | Required | Default | Description |
| ------------- | ------------- | ------------- | ------------- |
| org_id  | Yes  | | The organization UUID |
| page  | No  |1 | The page number for asset list |
| asset_type  | No  |[1,2,3,4] | The type of assets you want to filter by. For example, asset_type=[1,2,3,4]  |
| state  | No  |[0,1,2,3,4,5,6,7] | The state of vulnerabilities you want to filter by. For example, asset_type=[1,2,4]  |
| severity  | No  |[1,2,3,4,5] | The severity of vulnerabilities you want to filter by. For example, asset_type=[1,2,4,5]  |
| cve  | No  |  | The cve you want to filter vulnerabilities by  |
| assets  | No  | []| The asset IDs you want to filter vulnerabilities  |

**Returns**

```
VulnerabilityListResource
```

### get_vulnerability

**Expected**

| Name  | Required | Default | Description |
| ------------- | ------------- | ------------- | ------------- |
| org_id  | Yes  | | The organization UUID |
| asset_id  | Yes  || The asset ID |
| vulnerability_id  | yes  || The vulnerability ID |

**Returns**

```
VulnerabilityResource
```


### update_vulnerability

**Expected**

| Name  | Required | Default | Description |
| ------------- | ------------- | ------------- | ------------- |
| org_id  | Yes  | | The organization UUID |
| asset_id  | Yes  || The asset ID |
| vulnerability_id  | yes  || The vulnerability ID |
| state  | No  || The state of the vulnerability |
| severity  | No  || The severity of the vulnerability  |

**Returns**

```
VulnerabilityResource
```


### update_vulnerability_tags

**Expected**

| Name  | Required | Default | Description |
| ------------- | ------------- | ------------- | ------------- |
| org_id  | Yes  | | The organization UUID |
| asset_id  | Yes  || The asset ID |
| vulnerability_id  | yes  || The vulnerability ID |
| bug_tags  | yes  || List of tags |


**Returns**

```
VulnerabilityResource
```

# :hammer: Resources

### OrganizationResource

| Name  | Description |
| ------------- | ------------- |
| id  | UUID of organization  |
| name  | Name of the organization  |

### OrganizationListResource

| Name  | Description |
| ------------- | ------------- |
| count  | Total number of organizations for the current query |
| results  | List of OrganizationResource |

### AssetListResource

| Name  | Description |
| ------------- | ------------- |
| count  | Total number of assets for the current query |
| results  | List of AssetResource |

### AssetResource

| Name  | Description |
| ------------- | ------------- |
| id  | The ID of the asset |
| name  | The name of the asset |
| organization  | The organization ID of the asset |
| exposed  | The exposed state of the asset AssetExposureType |
| target  | The target the asset used for scanning |
| type  | The type the asset AssetType |
| cloud_type  | The cloud type of the asset |
| linked_assets  | Assets linked with the requested asset |
| data  | AssetInfoResource |

### AssetInfoResource

| Name  | Description |
| ------------- | ------------- |
| os  | The OS of the asset |
| cpe  | The cpe of the asset |
| netbios  | The netbios of the asset |
| hostname  | The hostname of the asset |
| ipaddress  | The ipaddress of the asset |
| mac_address  | The mac_address of the asset |


### VulnerabilityListResource

| Name  | Description |
| ------------- | ------------- |
| count  | Total number of vulnerabilities for the current query |
| results  | List of VulnerabilityResource |


### VulnerabilityResource

| Name  | Description |
| ------------- | ------------- |
| id  | The id of the vulnerability |
| title  | The title of the vulnerability |
| description  | The description of the vulnerability |
| steps_to_reproduce  | The steps_to_reproduce of the vulnerability |
| state  | VulnerabilityStateType |
| patch_available  | The mitigation of the vulnerability |
| mitigation  | if patch is avaialble |
| exploit_available  | if exploit is available |
| cwe  | the CWE list of the vulnerability |
| cvss  | if cvss score of the vulnerability |
| cve  | if cve list of the vulnerability |
| severity  | VulnerabilitySeverityType |
| asset  | the asset ID of the vulnerability |


# :flashlight: Types

### AssetType
| ID  | Name |
| ------------- | ------------- |
| 1  | web |
| 2  | Mobile |
| 3  | Network |
| 4 | Cloud |
| 5  | Others |

### SensitivityType
| ID  | Name |
| ------------- | ------------- |
| None | 0 |
| 1 | Low |
| 2  | Medium |
| 3 | High |

### AssetExposureType
| ID  | Name |
| ------------- | ------------- |
| 1 | Public |
| 2 | Private |


### VulnerabilitySeverityType
| ID  | Name |
| ------------- | ------------- |
| 1 | info |
| 2 | low |
| 3 | medium |
| 4 | high |
| 5 | critical |

### VulnerabilityStateType
| ID  | Name |
| ------------- | ------------- |
| 0 | new.   |
| 1 | active |
| 2 | resolved |
| 3 | duplicate |
| 4 | not_applicable |
| 5 | committed |
| 6 | accepted_risk |
| 7 | wont_fix |

