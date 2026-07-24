from enum import Enum


class SortField(str, Enum):
    NAME = "name"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    STATUS = "status"
    ASSET_TYPE = "asset_type"