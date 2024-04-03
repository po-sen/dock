from dock_cli.utils.utils import update_config, topological_sort


def test_update_config(mocker, mock_config_open, config_file):
    mock_config = mocker.Mock()
    update_config(mock_config, config_file)
    mock_config_open.assert_called_once_with(config_file, 'w', encoding='utf-8')
    mock_config.write.assert_called_once()


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
