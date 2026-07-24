from enum import Enum


class AssetType(str, Enum):
    DRONE = "DRONE"
    VEHICLE = "VEHICLE"
    CAMERA = "CAMERA"
    SENSOR = "SENSOR"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    OTHER = "OTHER"