import pytest
from dock_cli.utils.schema import SectionType

class TestChartHelper():
    def test_get_section_path(self, chart_helper, chart_section, test_repo):
        result = chart_helper.get_section_path(chart_section.section)
        assert result == test_repo / chart_section.section

    def test_is_valid_section_true(self, chart_helper, chart_section):
        result = chart_helper.is_valid_section(chart_section.section)
        assert result is True

    def test_is_valid_section_false(self, chart_helper, invalid_chart_section):
        result = chart_helper.is_valid_section(invalid_chart_section.section)
        assert result is False

    def test_validate_section(self, chart_helper, chart_section):
        result = chart_helper.validate_section(chart_section.section)
        assert result is None

    def test_validate_section_error(self, chart_helper, invalid_chart_section):
        with pytest.raises(AssertionError) as excinfo:
            chart_helper.validate_section(invalid_chart_section.section)
        assert str(excinfo.value) == f"Expected the section '{invalid_chart_section.section}' is valid."

    def test_get_section_file(self, chart_helper, chart_section, test_repo):
        result = chart_helper.get_section_file(chart_section.section)
        assert result == test_repo / chart_section.section / 'Chart.yaml'

    def test_get_section_type(self, chart_helper, chart_section):
        result = chart_helper.get_section_type(chart_section.section)
        assert result == SectionType.CHART

    def test_get_section_registry(self, chart_helper, chart_section):
        result = chart_helper.get_section_registry(chart_section.section)
        assert result == chart_section.registry

    def test_get_chart_name(self, chart_helper, chart_section):
        result = chart_helper.get_chart_name(chart_section.section)
        assert result == chart_section.name

    def test_get_chart_version(self, chart_helper, chart_section):
        result = chart_helper.get_chart_version(chart_section.section)
        assert result == chart_section.version

    def test_get_chart(self, chart_helper, chart_section):
        result = chart_helper.get_chart(chart_section.section)
        assert result == f'{chart_section.registry}/{chart_section.name}'

    def test_get_charts(self, chart_helper, chart_list):
        result = chart_helper.get_charts()
        assert result == chart_list

    def test_get_updated_charts(self, chart_helper, chart_list, initial_commit):
        result = chart_helper.get_updated_charts('HEAD', None)
        assert result == []
        result = chart_helper.get_updated_charts('HEAD', 'HEAD')
        assert result == []
        result = chart_helper.get_updated_charts(initial_commit, initial_commit)
        assert result == []
        result = chart_helper.get_updated_charts(initial_commit, None)
        assert result == chart_list

    def test_get_chart_archive_file(self, chart_helper, chart_section):
        result = chart_helper.get_chart_archive_file(chart_section.section, '.')
        assert result == f'./{chart_section.name}-{chart_section.version}.tgz'


class TestImageHelper():
    def test_get_section_path(self, image_helper, image_section, test_repo):
        result = image_helper.get_section_path(image_section.section)
        assert result == test_repo / image_section.section

    def test_is_valid_section_true(self, image_helper, image_section):
        result = image_helper.is_valid_section(image_section.section)
        assert result is True

    def test_is_valid_section_false(self, image_helper, invalid_image_section):
        result = image_helper.is_valid_section(invalid_image_section.section)
        assert result is False

    def test_validate_section(self, image_helper, image_section):
        result = image_helper.validate_section(image_section.section)
        assert result is None

    def test_validate_section_error(self, image_helper, invalid_image_section):
        with pytest.raises(AssertionError) as excinfo:
            image_helper.validate_section(invalid_image_section.section)
        assert str(excinfo.value) == f"Expected the section '{invalid_image_section.section}' is valid."

    def test_get_section_file(self, image_helper, image_section, test_repo):
        result = image_helper.get_section_file(image_section.section)
        assert result == test_repo / image_section.section / 'Dockerfile'

    def test_get_section_type(self, image_helper, image_section):
        result = image_helper.get_section_type(image_section.section)
        assert result == SectionType.IMAGE

    def test_get_section_name(self, image_helper, image_section):
        result = image_helper.get_section_name(image_section.section)
        assert result == image_section.name

    def test_get_section_dependencies(self, image_helper, image_section):
        result = image_helper.get_section_dependencies(image_section.section)
        assert isinstance(result, list)

    def test_get_section_registry(self, image_helper, image_section):
        result = image_helper.get_section_registry(image_section.section)
        assert result == image_section.registry

    def test_get_image(self, image_helper, image_section):
        result = image_helper.get_image(image_section.section, 'latest')
        assert result == f'{image_section.registry}/{image_section.name}:latest'

    def test_get_images(self, image_helper, image_list):
        result = image_helper.get_images()
        assert result == image_list

    def test_get_updated_images(self, image_helper, image_list, initial_commit):
        result = image_helper.get_updated_images('HEAD', None)
        assert result == []
        result = image_helper.get_updated_images('HEAD', 'HEAD')
        assert result == []
        result = image_helper.get_updated_images(initial_commit, initial_commit)
        assert result == []
        result = image_helper.get_updated_images(initial_commit, None)
        assert result == image_list
