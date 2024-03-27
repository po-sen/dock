def test_chart_list(runner, env, dock, chart_list):
    result = runner.invoke(dock, ['chart', 'list'], env=env)
    assert result.exit_code == 0
    assert result.output == ''.join(f'{chart}\n' for chart in chart_list)

def test_chart_diff(runner, env, dock):
    result = runner.invoke(dock, ['chart', 'diff', 'HEAD', 'HEAD'], env=env)
    assert result.exit_code == 0
    assert result.output == ''

def test_chart_diff_initial_commit(runner, env, dock, initial_commit, chart_list):
    result = runner.invoke(dock, ['chart', 'diff', initial_commit, 'HEAD'], env=env)
    assert result.exit_code == 0
    assert result.output == ''.join(f'{chart}\n' for chart in chart_list)

def test_chart_show(runner, env, dock, chart_section):
    result = runner.invoke(dock, ['chart', 'show', chart_section.section], env=env)
    assert result.exit_code == 0
    assert result.output == f'{chart_section.registry}/{chart_section.name}\n'

def test_chart_package(runner, env, dock, mock_commands_run, chart_section, config_file):
    # pylint: disable=too-many-arguments
    result = runner.invoke(dock, ['chart', 'package', chart_section.section, '--destination', '.'], env=env)
    mock_commands_run.assert_called_once_with(['helm', 'package', config_file.parent / chart_section.section,
                                               '--destination', '.'])
    assert result.exit_code == 0

def test_chart_package_list(runner, env, dock, mock_commands_run, chart_list, config_file):
    # pylint: disable=too-many-arguments
    result = runner.invoke(dock, ['chart', 'package', *chart_list, '--destination', '.'], env=env)
    for section in chart_list:
        mock_commands_run.assert_any_call(['helm', 'package', config_file.parent / section, '--destination', '.'])
    assert result.exit_code == 0

def test_chart_push(runner, env, dock, mock_commands_run, chart_section):
    result = runner.invoke(dock, ['chart', 'push', chart_section.section, '--destination', '.'], env=env)
    mock_commands_run.assert_called_once_with(['helm', 'push', f'./{chart_section.name}-{chart_section.version}.tgz',
                                               chart_section.registry])
    assert result.exit_code == 0

def test_chart_config(runner, env, dock, mock_update_config):
    result = runner.invoke(dock, ['chart', 'config'], env=env)
    mock_update_config.assert_not_called()
    assert result.exit_code == 0
    assert result.output != ''

def test_chart_config_init(runner, env, dock, mock_update_config):
    result = runner.invoke(dock, ['chart', 'config', 'init', '--registry', 'mew'], env=env)
    mock_update_config.assert_called_once()
    assert result.exit_code == 0
    assert result.output != ''

def test_chart_config_add(runner, env, dock, mock_update_config, valid_chart_section, config_file):
    # pylint: disable=too-many-arguments
    path = str(config_file.parent / valid_chart_section.section)
    result = runner.invoke(dock, ['chart', 'config', 'add', path], env=env)
    mock_update_config.assert_called_once()
    assert result.exit_code == 0
    assert result.output != ''

def test_chart_config_add_error(runner, env, dock, mock_update_config, invalid_chart_section, config_file):
    # pylint: disable=too-many-arguments
    path = str(config_file.parent / invalid_chart_section.section)
    result = runner.invoke(dock, ['chart', 'config', 'add', path], env=env)
    mock_update_config.assert_not_called()
    assert result.exit_code == 2
