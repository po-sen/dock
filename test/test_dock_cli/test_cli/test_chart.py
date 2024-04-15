from helpers import invoke_cli

def test_chart_list(dock, env, chart_list):
    output = invoke_cli(dock, ['chart', 'list'], env=env)
    assert output == ''.join(f'{section}\n' for section in chart_list)

def test_chart_diff(dock, env):
    output = invoke_cli(dock, ['chart', 'diff', 'HEAD', 'HEAD'], env=env)
    assert output == ''

def test_chart_diff_initial_commit(dock, env, chart_list, initial_commit):
    output = invoke_cli(dock, ['chart', 'diff', initial_commit, 'HEAD'], env=env)
    assert output == ''.join(f'{section}\n' for section in chart_list)

def test_chart_show(dock, env, chart_section):
    output = invoke_cli(dock, ['chart', 'show', chart_section.section], env=env)
    assert output == f'{chart_section.registry}/{chart_section.name}\n'

def test_chart_package(dock, env, chart_section, config_file, mock_commands_run):
    output = invoke_cli(dock, ['chart', 'package', chart_section.section, '--destination', '.'], env=env)
    mock_commands_run.assert_called_once_with(['helm', 'package', config_file.parent / chart_section.section,
                                               '--destination', '.'])
    assert output == ''

def test_chart_package_list(dock, env, chart_list, config_file, mock_commands_run):
    output = invoke_cli(dock, ['chart', 'package', *chart_list, '--destination', '.'], env=env)
    for section in chart_list:
        mock_commands_run.assert_any_call(['helm', 'package', config_file.parent / section, '--destination', '.'])
    assert output == ''

def test_chart_push(dock, env, chart_section, mock_commands_run):
    output = invoke_cli(dock, ['chart', 'push', chart_section.section, '--destination', '.'], env=env)
    mock_commands_run.assert_called_once_with(['helm', 'push', f'./{chart_section.name}-{chart_section.version}.tgz',
                                               chart_section.registry])
    assert output == ''

def test_chart_config_view(dock, env, chart_list, mock_update_config):
    output = invoke_cli(dock, ['chart', 'config', 'view'], env=env)
    mock_update_config.assert_not_called()
    for section in chart_list:
        assert f'{section}:\n' in output

def test_chart_config_view_no_charts(dock, env_dne, mock_update_config):
    output = invoke_cli(dock, ['chart', 'config', 'view'], env=env_dne)
    mock_update_config.assert_not_called()
    assert output == ''

def test_chart_config_set(dock, env, valid_chart_section, config_file, mock_update_config, mock_click_confirm):
    # pylint: disable=too-many-arguments
    path = str(config_file.parent / valid_chart_section.section)
    output = invoke_cli(dock, ['chart', 'config', 'set', path], env=env)
    if mock_click_confirm.return_value:
        mock_update_config.assert_called_once()
    else:
        mock_update_config.assert_not_called()
    assert f'Set [{valid_chart_section.section}] type = chart\n' in output
    assert f'{valid_chart_section.section}:\n' in output

def test_chart_config_set_error(dock, env, invalid_chart_section, config_file, mock_update_config, mock_click_confirm):
    # pylint: disable=too-many-arguments
    path = str(config_file.parent / invalid_chart_section.section)
    output = invoke_cli(dock, ['chart', 'config', 'set', path], env=env, expected_exit_code=2)
    mock_update_config.assert_not_called()
    mock_click_confirm.assert_not_called()
    assert "Error: Invalid value for 'SECTION':" in output

def test_chart_config_set_registry(dock, env, mock_update_config, mock_click_confirm):
    output = invoke_cli(dock, ['chart', 'config', 'set-registry', 'mew'], env=env)
    if mock_click_confirm.return_value:
        mock_update_config.assert_called_once()
    else:
        mock_update_config.assert_not_called()
    assert output.splitlines()[0] == 'Set [DEFAULT] oci-registry = mew'
