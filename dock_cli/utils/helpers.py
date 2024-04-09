import dataclasses
import functools
import pathlib
import re
import click
from dock_cli.utils import commands as cmd
from dock_cli.utils.schema import ChartConfigOptions as Chart, ImageConfigOptions as Image, SectionType
from dock_cli.utils.utils import topological_sort


@dataclasses.dataclass()
class Command():
    __slots__ = ['docker', 'helm', 'git']

    docker: str
    helm: str
    git: str

    def __post_init__(self):
        self.docker = 'docker' if self.docker is None else self.docker
        self.helm = 'helm' if self.helm is None else self.helm
        self.git = 'git' if self.git is None else self.git


class OrderedGroup(click.Group):
    def list_commands(self, _ctx):
        return self.commands


class ConfigHelper():
    def __init__(self, config, config_dir, command):
        self.config = config
        self.config_dir = config_dir
        self.command = command

    def get_section_path(self, section):
        return self.config_dir / pathlib.Path(section)

    def validate_section(self, section):
        assert section in self.config, (
               f"The section '{section}' is not in the configuration.")
        assert not pathlib.Path(section).is_absolute(), (
               f"The section '{section}' should be a relative path.")

    def is_valid_section(self, section):
        try:
            self.validate_section(section)
        except AssertionError:
            return False
        return True

    @functools.lru_cache()
    def is_updated_section(self, section, commit1, commit2):
        return cmd.getoutput([self.command.git, 'diff', commit1, commit2, '--', self.get_section_path(section)]) != ''


class ChartHelper(ConfigHelper):
    def get_section_file(self, section):
        return self.get_section_path(section) / 'Chart.yaml'

    def get_section_type(self, section):
        return self.config.get(section, Chart.TYPE, fallback='')

    def get_section_registry(self, section):
        return self.config.get(section, Chart.REGISTRY, fallback='')

    def validate_section(self, section):
        super().validate_section(section)
        assert self.get_section_file(section).exists(), (
               f"File does not exist: {self.get_section_file(section)}.")
        assert self.get_section_type(section) == SectionType.CHART, (
               f"The section '{section}' type should be {SectionType.CHART}.")
        assert self.get_section_registry(section), (
               f"The section '{section}' registry should exist.")

    def get_chart_info(self, section):
        return cmd.getoutput([self.command.helm, 'show', 'chart', self.get_section_path(section)])

    def get_chart_name(self, section):
        return re.search(r'^name:\s*(\S+)', self.get_chart_info(section), flags=re.MULTILINE).group(1)

    def get_chart_version(self, section):
        return re.search(r'^version:\s*(\S+)', self.get_chart_info(section), flags=re.MULTILINE).group(1)

    def get_chart(self, section):
        return f'{self.get_section_registry(section)}/{self.get_chart_name(section)}'

    def get_charts(self):
        return [section for section in self.config.sections() if self.is_valid_section(section)]

    def get_updated_charts(self, commit1, commit2):
        return [section for section in self.get_charts() if self.is_updated_section(section, commit1, commit2)]

    def get_chart_archive_file(self, section, destination):
        return f'{destination}/{self.get_chart_name(section)}-{self.get_chart_version(section)}.tgz'


class ImageHelper(ConfigHelper):
    def get_section_file(self, section):
        return self.get_section_path(section) / self.config.get(section, Image.FILE, fallback='Dockerfile')

    def get_section_type(self, section):
        return self.config.get(section, Image.TYPE, fallback='')

    def get_section_name(self, section):
        return self.config.get(section, Image.NAME, fallback=pathlib.Path(section).name)

    def get_section_dependencies(self, section):
        return self.config.get(section, Image.DEPENDS_ON, fallback='').strip().splitlines()

    def get_section_registry(self, section):
        return self.config.get(section, Image.REGISTRY, fallback='')

    def validate_section(self, section):
        super().validate_section(section)
        assert self.get_section_file(section).exists(), (
               f"File does not exist: {self.get_section_file(section)}.")
        assert self.get_section_type(section) == SectionType.IMAGE, (
               f"The section '{section}' type should be {SectionType.IMAGE}.")
        assert self.get_section_registry(section), (
               f"The section '{section}' registry should exist.")

    def get_image(self, section, image_tag):
        return f'{self.get_section_registry(section)}/{self.get_section_name(section)}:{image_tag}'

    def get_images(self):
        return topological_sort({section: set(self.get_section_dependencies(section))
                                 for section in self.config.sections() if self.is_valid_section(section)})

    def get_updated_images(self, commit1, commit2):
        return [section for section in self.get_images() if self.is_updated_section(section, commit1, commit2)
                or any(self.is_updated_section(depends_on, commit1, commit2)
                       for depends_on in self.get_section_dependencies(section))]
