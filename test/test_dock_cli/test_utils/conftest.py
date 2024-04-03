import configparser
import pytest
from dock_cli.utils.helpers import Command, ChartHelper, ImageHelper

@pytest.fixture(scope='function')
def chart_helper(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return ChartHelper(config, config_file.parent, Command(None, None, None))

@pytest.fixture(scope='function')
def image_helper(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return ImageHelper(config, config_file.parent, Command(None, None, None))
