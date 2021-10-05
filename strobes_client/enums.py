from enum import Enum
class RequestEnums(Enum):
    user_agent = 'strobes-python-client'
    app_port = 443
    app_scheme = "https"
    app_host = "app.strobes.co"
class VulnerabilityTypeEnum(Enum):

    code = 'code'
    code_bug_level = 1
    web = 'web'
    web_bug_level = 2
    network = 'network'
    network_bug_level = 4
    cloud = 'cloud'
    cloud_bug_level = 5
    package = 'package'
    package_bug_level = 6


