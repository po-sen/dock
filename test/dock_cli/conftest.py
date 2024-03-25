import configparser
import dataclasses
import pathlib
import pytest
from click.testing import CliRunner
from dock_cli.main import cli
from dock_cli.utils.helpers import Command, ChartHelper, ImageHelper

TEST_REPO = pathlib.Path(__file__).resolve().parent.parent / 'repo'
TEST_REPO_CONFIG = TEST_REPO / 'dock.ini'

@dataclasses.dataclass()
class ChartSection():
    section: str
    name: str = ''
    version: str = '0.1.0'
    registry: str = 'oci://registry-1.docker.io/namespace'

@dataclasses.dataclass()
class ImageSection():
    section: str
    name: str = ''
    registry: str = 'namespace'

@pytest.fixture(scope='function')
def runner():
    return CliRunner()

@pytest.fixture(scope='session')
def dock():
    return cli

@pytest.fixture(scope='function',
                params=['-h', '--help'])
def help_option(request):
    return request.param

@pytest.fixture(scope='function')
def test_repo():
    return TEST_REPO

@pytest.fixture(scope='function')
def test_repo_config():
    return TEST_REPO_CONFIG

@pytest.fixture(scope='function')
def chart_helper():
    config = configparser.ConfigParser()
    config.read(TEST_REPO_CONFIG)
    return ChartHelper(config, TEST_REPO, Command())

@pytest.fixture(scope='function',
                params=[ChartSection('charts/chart-1', 'chart-1'),
                        ChartSection('charts/chart-2', 'chart-2'),
                        ChartSection('charts/chart-3', 'chart-3'),
                        ChartSection('charts/chart-4', 'chart-4')])
def chart_section(request):
    return request.param

@pytest.fixture(scope='function',
                params=[ChartSection('charts/chart-mew'),
                        ChartSection('charts/chart-omg')])
def invalid_chart_section(request):
    return request.param

@pytest.fixture(scope='function')
def chart_list():
    return ['charts/chart-1',
            'charts/chart-2',
            'charts/chart-3',
            'charts/chart-4']

@pytest.fixture(scope='function')
def image_helper():
    config = configparser.ConfigParser()
    config.read(TEST_REPO_CONFIG)
    return ImageHelper(config, TEST_REPO, Command())

@pytest.fixture(scope='function',
                params=[ImageSection('images/image-1', 'image-1'),
                        ImageSection('images/image-2', 'image-2'),
                        ImageSection('images/image-3', 'image-3'),
                        ImageSection('images/image-4', 'custom-image-name')])
def image_section(request):
    return request.param

@pytest.fixture(scope='function',
                params=[ImageSection('images/image-mew'),
                        ImageSection('images/image-omg')])
def invalid_image_section(request):
    return request.param

@pytest.fixture(scope='function')
def image_list():
    return ['images/image-1',
            'images/image-4',
            'images/image-3',
            'images/image-2']

@pytest.fixture(scope='function')
def initial_commit():
    return '472afe80cb490b6827e775bcc8b0a42eaee27db5'
