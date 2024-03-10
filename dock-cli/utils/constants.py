import enum

class Command(enum.Enum):
    DOCKER = 'docker'
    GIT = 'git'

class SessionType(enum.Enum):
    IMAGE = 'image'

class Image(enum.Enum):
    FILE = 'file'
    NAME = 'name'
    TYPE = 'type'
    REGISTRY = 'registry'
    DEPENDS_ON = 'depends_on'
