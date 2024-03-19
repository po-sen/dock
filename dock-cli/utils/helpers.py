import dataclasses
import pathlib
import re
import click
from utils import commands as cmd
from utils.schema import ChartConfigOptions as Chart, ImageConfigOptions as Image, SectionType
from utils.utils import topological_sort


@dataclasses.dataclass()
class Command():
    docker: str = 'docker'
    helm: str = 'helm'
    git: str = 'git'


class OrderedGroup(click.Group):
    def list_commands(self, _ctx):
        return self.commands


class ConfigHelper():
    def __init__(self, config, config_file, command):
        self.config = config
        self.parent = pathlib.Path(config_file).parent
        self.command = command

    def get_section_path(self, section):
        return self.parent / pathlib.Path(section)

    def is_valid_section(self, section):
        return section in self.config

    def validate_section(self, section):
        assert self.is_valid_section(section), f"Expected the section '{section}' is valid."


class ChartHelper(ConfigHelper):
    def get_section_file(self, section):
        return self.get_section_path(section) / self.config.get(section, Chart.FILE.value, fallback='Chart.yaml')

    def get_section_type(self, section):
        return self.config.get(section, Chart.TYPE.value, fallback='')

    def get_section_registry(self, section):
        return self.config.get(section, Chart.REGISTRY.value, fallback='')

    def is_valid_section(self, section):
        if not self.get_section_file(section).exists():
            return False
        if self.get_section_type(section) != SectionType.CHART.value:
            return False
        if not self.get_section_registry(section):
            return False
        return True

    def get_chart_info(self, section):
        self.validate_section(section)
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
        return [section for section in self.get_charts()
                if cmd.getoutput([self.command.git, 'diff', commit1, commit2, self.get_section_path(section)])]

    def get_chart_archive_file(self, section, destination):
        return f'{destination}/{self.get_chart_name(section)}-{self.get_chart_version(section)}.tgz'


class ImageHelper(ConfigHelper):
    def get_section_file(self, section):
        return self.get_section_path(section) / self.config.get(section, Image.FILE.value, fallback='Dockerfile')

    def get_section_type(self, section):
        return self.config.get(section, Image.TYPE.value, fallback='')

    def get_section_name(self, section):
        return self.config.get(section, Image.NAME.value, fallback=pathlib.Path(section).name)

    def get_section_dependencies(self, section):
        return self.config.get(section, Image.DEPENDS_ON.value, fallback='').strip().splitlines()

    def get_section_registry(self, section):
        return self.config.get(section, Image.REGISTRY.value, fallback='')

    def is_valid_section(self, section):
        if not self.get_section_file(section).exists():
            return False
        if self.get_section_type(section) != SectionType.IMAGE.value:
            return False
        if not self.get_section_registry(section):
            return False
        return True

    def get_image(self, section, image_tag):
        self.validate_section(section)
        return f'{self.get_section_registry(section)}/{self.get_section_name(section)}:{image_tag}'

    def get_images(self):
        return topological_sort({section: set(self.get_section_dependencies(section))
                                 for section in self.config.sections() if self.is_valid_section(section)})

    def is_updated_section(self, section, commit1, commit2):
        if (self.is_valid_section(section) and
            cmd.getoutput([self.command.git, 'diff', commit1, commit2, self.get_section_path(section)])):
            return True
        return any(self.is_updated_section(depends_on, commit1, commit2)
                   for depends_on in self.get_section_dependencies(section))

    def get_updated_images(self, commit1, commit2):
        return [section for section in self.get_images() if self.is_updated_section(section, commit1, commit2)]
