import enum

class Chart(enum.Enum):
    REGISTRY = 'oci registry'
    FILE = 'file'
    TYPE = 'type'

class Image(enum.Enum):
    REGISTRY = 'registry'
    FILE = 'file'
    NAME = 'name'
    TYPE = 'type'
    DEPENDS_ON = 'depends on'

class SessionType(enum.Enum):
    CHART = 'chart'
    IMAGE = 'image'
