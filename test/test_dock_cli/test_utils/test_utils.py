import click
from dock_cli.utils.utils import update_config, topological_sort


def test_update_config(mocker, config_file, mock_config_open, mock_click_confirm, mock_click_echo):
    mock_config = mocker.Mock()
    update_config(mock_config, config_file)
    if mock_click_confirm.return_value:
        mock_config_open.assert_called_once_with(config_file, 'w', encoding='utf-8')
        mock_config.write.assert_called_once()
        mock_click_echo.assert_called_once_with(click.style('  Successfully updated.', fg='green'))
    else:
        mock_config_open.assert_not_called()
        mock_config.write.assert_not_called()
        mock_click_echo.assert_called_once_with(click.style('  Cancel the update.', fg='yellow'))


def test_update_config_assume_yes(mocker, config_file, mock_config_open, mock_click_confirm, mock_click_echo):
    mock_config = mocker.Mock()
    update_config(mock_config, config_file, assume_yes=True)
    mock_click_confirm.assert_not_called()
    mock_config_open.assert_called_once_with(config_file, 'w', encoding='utf-8')
    mock_config.write.assert_called_once()
    mock_click_echo.assert_not_called()


class TestTopologicalSort():
    def test_linear_dependencies(self):
        dependencies = {
            'a': ['b'],
            'b': ['c'],
            'c': [],
        }
        assert topological_sort(dependencies) == ['c', 'b', 'a']

    def test_complex_dependencies(self):
        dependencies = {
            'a': ['b'],
            'b': ['c', 'd'],
            'c': ['d'],
            'd': [],
        }
        result = topological_sort(dependencies)
        assert result.index('d') < result.index('c')
        assert result.index('c') < result.index('b')
        assert result.index('b') < result.index('a')

    def test_no_dependencies(self):
        dependencies = {
            'a': [],
            'b': [],
            'c': [],
        }
        result = set(topological_sort(dependencies))
        assert result == {'a', 'b', 'c'}

    def test_dependencies_not_as_nodes(self):
        dependencies = {
            'a': ['b'],
            'b': ['c'],
            'c': ['d'],
        }
        result = topological_sort(dependencies)
        assert result == ['c', 'b', 'a']
