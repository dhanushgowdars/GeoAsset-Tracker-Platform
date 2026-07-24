from enum import Enum


class AssetStatus(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    MAINTENANCE = "MAINTENANCE"
    RETIRED = "RETIRED"