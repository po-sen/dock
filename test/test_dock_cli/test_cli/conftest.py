import pytest

@pytest.fixture(scope='function')
def env(config_file):
    return {'DOCK_CONFIG_FILE': str(config_file)}

@pytest.fixture(scope='function')
def env_init(config_file_init):
    return {'DOCK_CONFIG_FILE': str(config_file_init)}
