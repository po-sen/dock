from helpers import invoke_cli

def test_image_list(dock, env, image_list):
    output = invoke_cli(dock, ['image', 'list'], env=env)
    assert output == ''.join(f'{section}\n' for section in image_list)

def test_image_diff(dock, env):
    output = invoke_cli(dock, ['image', 'diff', 'HEAD', 'HEAD'], env=env)
    assert output == ''

def test_image_diff_initial_commit(dock, env, image_list, initial_commit):
    output = invoke_cli(dock, ['image', 'diff', initial_commit, 'HEAD'], env=env)
    assert output == ''.join(f'{section}\n' for section in image_list)

def test_image_show(dock, env, image_section):
    output = invoke_cli(dock, ['image', 'show', image_section.section], env=env)
    assert output == f'{image_section.registry}/{image_section.name}:latest\n'
    output = invoke_cli(dock, ['image', 'show', image_section.section, 'mew'], env=env)
    assert output == f'{image_section.registry}/{image_section.name}:mew\n'

def test_image_build(dock, env, image_section, config_file, mock_commands_run):
    output = invoke_cli(dock, ['image', 'build', image_section.section], env=env)
    mock_commands_run.assert_called_with(['docker', 'build', config_file.parent / image_section.section,
                                          '--file', config_file.parent / image_section.section / 'Dockerfile',
                                          '--tag', f'{image_section.registry}/{image_section.name}:latest'])
    assert output == ''
    output = invoke_cli(dock, ['image', 'build', image_section.section, '--tag', 'mew', '--tag', 'omg'], env=env)
    mock_commands_run.assert_called_with(['docker', 'build', config_file.parent / image_section.section,
                                          '--file', config_file.parent / image_section.section / 'Dockerfile',
                                          '--tag', f'{image_section.registry}/{image_section.name}:mew',
                                          '--tag', f'{image_section.registry}/{image_section.name}:omg'])
    assert output == ''

def test_image_build_list(dock, env, image_list, image_section, config_file, mock_commands_run):
    # pylint: disable=too-many-arguments
    output = invoke_cli(dock, ['image', 'build', *image_list], env=env)
    mock_commands_run.assert_any_call(['docker', 'build', config_file.parent / image_section.section,
                                       '--file', config_file.parent / image_section.section / 'Dockerfile',
                                       '--tag', f'{image_section.registry}/{image_section.name}:latest'])
    assert output == ''

def test_image_push(dock, env, image_section, mock_commands_run):
    output = invoke_cli(dock, ['image', 'push', image_section.section], env=env)
    mock_commands_run.assert_called_once_with(['docker', 'push',
                                               f'{image_section.registry}/{image_section.name}:latest'])
    assert output == ''

def test_image_clean(dock, env, image_section, mock_commands_run):
    output = invoke_cli(dock, ['image', 'clean', image_section.section], env=env)
    mock_commands_run.assert_called_once_with(['docker', 'rmi', '--force',
                                               f'{image_section.registry}/{image_section.name}:latest'])
    assert output == ''

def test_image_view(dock, env, image_list, mock_update_config):
    output = invoke_cli(dock, ['image', 'view'], env=env)
    mock_update_config.assert_not_called()
    for section in image_list:
        assert f'{section}:\n' in output

def test_image_view_no_images(dock, env_init, mock_update_config):
    output = invoke_cli(dock, ['image', 'view'], env=env_init)
    mock_update_config.assert_not_called()
    assert output == ''

def test_image_set_registry(dock, env, mock_update_config):
    output = invoke_cli(dock, ['image', 'set-registry', 'mew'], env=env)
    mock_update_config.assert_called_once()
    assert output.splitlines()[0] == '  Set [DEFAULT] registry = mew'

def test_image_set(dock, env, valid_image_section, config_file, mock_update_config):
    path = str(config_file.parent / valid_image_section.section)
    output = invoke_cli(dock, ['image', 'set', path], env=env)
    mock_update_config.assert_called_once()
    assert f'  Set [{valid_image_section.section}] type = image\n' in output

def test_image_set_without_config_file(dock, env_init, valid_image_section, config_file, mock_update_config):
    path = str(config_file.parent / valid_image_section.section)
    output = invoke_cli(dock, ['image', 'set', path, '--registry=namespace'], env=env_init)
    mock_update_config.assert_called_once()
    assert f'  Set [{valid_image_section.section}] type = image\n' in output
    assert f'  Set [{valid_image_section.section}] registry = namespace\n' in output

def test_image_set_with_params_1(dock, env, valid_image_section, config_file, mock_update_config):
    path = str(config_file.parent / valid_image_section.section)
    output = invoke_cli(dock, ['image', 'set', path,
                               f'--image-name={valid_image_section.name}',
                               f'--depends-on={config_file.parent}/images/image-1/'], env=env)
    mock_update_config.assert_called_once()
    assert f'  Set [{valid_image_section.section}] type = image\n' in output
    assert f'  Set [{valid_image_section.section}] image-name = {valid_image_section.name}\n' in output
    assert f'  Set [{valid_image_section.section}] depends-on = images/image-1\n' in output

def test_image_set_with_params_2(dock, env, valid_image_section, config_file, mock_update_config):
    path = str(config_file.parent / valid_image_section.section)
    output = invoke_cli(dock, ['image', 'set', path,
                               '--image-file=Dockerfile',
                               '--registry=namespace',
                               f'--image-name={valid_image_section.name}',
                               f'--depends-on={config_file.parent}/charts/chart-1',
                               f'--depends-on={config_file.parent}/dock.ini',
                               f'--depends-on={config_file.parent}/.'], env=env)
    mock_update_config.assert_called_once()
    assert f'  Set [{valid_image_section.section}] type = image\n' in output
    assert f'  Set [{valid_image_section.section}] registry = namespace\n' in output
    assert f'  Set [{valid_image_section.section}] image-file = Dockerfile\n' in output
    assert f'  Set [{valid_image_section.section}] image-name = {valid_image_section.name}\n' in output
    assert f'  Set [{valid_image_section.section}] depends-on = \ncharts/chart-1\ndock.ini\n.\n' in output

def test_image_set_error(dock, env, invalid_image_section, config_file, mock_update_config):
    # pylint: disable=too-many-arguments
    path = str(config_file.parent / invalid_image_section.section)
    output = invoke_cli(dock, ['image', 'set', path], env=env, expected_exit_code=2)
    mock_update_config.assert_not_called()
    assert "Error: Invalid value for 'SECTION':" in output

def test_image__unset(dock, env, image_section, mock_update_config):
    output = invoke_cli(dock, ['image', 'unset', image_section.section], env=env)
    mock_update_config.assert_called_once()
    assert f'  Unset [{image_section.section}]' in output

def test_image_unset_error(dock, env, invalid_image_section, mock_update_config):
    output = invoke_cli(dock, ['image', 'unset', invalid_image_section.section],
                        env=env, expected_exit_code=2)
    mock_update_config.assert_not_called()
    assert f'Error: The section [{invalid_image_section.section}] is not in the configuration.' in output
