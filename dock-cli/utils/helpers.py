import pathlib
from utils import commands as cmd
from utils.constants import SessionType, Image

class ImageHelper():
    def __init__(self, config, config_file):
        self.config = config
        self.parent = pathlib.Path(config_file).parent

    def get_section_path(self, section):
        return self.parent / pathlib.Path(section)

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
        if self.get_section_type(section) != SessionType.IMAGE.value:
            return False
        if not self.get_section_registry(section):
            return False
        if not self.get_section_file(section).exists():
            return False
        return True

    def get_images(self):
        return [section for section in self.config.sections() if self.is_valid_section(section)]

    def get_updated_images(self, git, commit1, commit2):
        return [section for section in self.get_images()
                if cmd.getoutput([git, 'diff', commit1, commit2, self.get_section_path(section)])]

    def get_image_name(self, section, image_tag):
        assert self.is_valid_section(section), f"Expected the section '{section}' to be in the list {self.get_images()}"
        return f'{self.get_section_registry(section)}/{self.get_section_name(section)}:{image_tag}'
