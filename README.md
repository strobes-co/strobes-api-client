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

#### list_organizations

**Expected**

| Name  | Required | Default | Description |
| ------------- | ------------- | ------------- | ------------- |
| page  | No  | 1 | The page number for organization list|

**Returns**

```
List[OrganizationResource]
```


#### get_organization

**Expected**

| Name  | Required | Default | Description |
| ------------- | ------------- | ------------- | ------------- |
| org_id  | Yes  | | The organization UUID |

**Returns**

```
OrganizationResource
```

#### get_assets

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

#### get_asset

**Expected**

| Name  | Required | Default | Description |
| ------------- | ------------- | ------------- | ------------- |
| org_id  | Yes  | | The organization UUID |
| asset_id  | Yes  || The asset ID |

**Returns**

```
AssetResource
```

#### update_asset

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
OrganizationResource
```

# :hammer: Resources

#### OrganizationResource

| Name  | Description |
| ------------- | ------------- |
| id  | UUID of organization  |
| name  | Name of the organization  |

#### OrganizationListResource

| Name  | Description |
| ------------- | ------------- |
| page  | Page number of the current results |
| results  | List of <OrganizationResource> |

# :flashlight: Types

### AssetType
| ID  | Name |
| ------------- | ------------- |
| 1  | web |
| 2  | Mobile |
| 3  | Network |
| 4 | Cloud |
| 5  | Others |

#### SensitivityType
| ID  | Name |
| ------------- | ------------- |
| None | 0 |
| 1 | Low |
| 2  | Medium |
| 3 | High |

#### AssetExposureType
| ID  | Name |
| ------------- | ------------- |
| 1 | Public |
| 2 | Private |

