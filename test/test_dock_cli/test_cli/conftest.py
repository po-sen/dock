import pytest

@pytest.fixture(scope='function')
def env(config_file):
    return {'DOCK_CONFIG_FILE': str(config_file)}
