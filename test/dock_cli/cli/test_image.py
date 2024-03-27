def test_image_list(runner, env, dock, image_list):
    result = runner.invoke(dock, ['image', 'list'], env=env)
    assert result.exit_code == 0
    assert result.output == ''.join(f'{image}\n' for image in image_list)

def test_image_diff(runner, env, dock):
    result = runner.invoke(dock, ['image', 'diff', 'HEAD', 'HEAD'], env=env)
    assert result.exit_code == 0
    assert result.output == ''

def test_image_diff_initial_commit(runner, env, dock, initial_commit, image_list):
    result = runner.invoke(dock, ['image', 'diff', initial_commit, 'HEAD'], env=env)
    assert result.exit_code == 0
    assert result.output == ''.join(f'{image}\n' for image in image_list)

def test_image_show(runner, env, dock, image_section):
    result = runner.invoke(dock, ['image', 'show', image_section.section], env=env)
    assert result.exit_code == 0
    assert result.output == f'{image_section.registry}/{image_section.name}:latest\n'
    result = runner.invoke(dock, ['image', 'show', image_section.section, 'mew'], env=env)
    assert result.exit_code == 0
    assert result.output == f'{image_section.registry}/{image_section.name}:mew\n'

def test_image_build(runner, env, dock, mock_commands_run, image_section, config_file):
    # pylint: disable=too-many-arguments
    result = runner.invoke(dock, ['image', 'build', image_section.section], env=env)
    mock_commands_run.assert_called_with(['docker', 'build', config_file.parent / image_section.section,
                                          '--file', config_file.parent / image_section.section / 'Dockerfile',
                                          '--tag', f'{image_section.registry}/{image_section.name}:latest'])
    assert result.exit_code == 0
    result = runner.invoke(dock, ['image', 'build', image_section.section, '--tag', 'mew', '--tag', 'omg'], env=env)
    mock_commands_run.assert_called_with(['docker', 'build', config_file.parent / image_section.section,
                                          '--file', config_file.parent / image_section.section / 'Dockerfile',
                                          '--tag', f'{image_section.registry}/{image_section.name}:mew',
                                          '--tag', f'{image_section.registry}/{image_section.name}:omg'])
    assert result.exit_code == 0

def test_image_build_list(runner, env, dock, mock_commands_run, image_list, image_section, config_file):
    # pylint: disable=too-many-arguments
    result = runner.invoke(dock, ['image', 'build', *image_list], env=env)
    mock_commands_run.assert_any_call(['docker', 'build', config_file.parent / image_section.section,
                                       '--file', config_file.parent / image_section.section / 'Dockerfile',
                                       '--tag', f'{image_section.registry}/{image_section.name}:latest'])
    assert result.exit_code == 0

def test_image_push(runner, env, dock, mock_commands_run, image_section):
    result = runner.invoke(dock, ['image', 'push', image_section.section], env=env)
    mock_commands_run.assert_called_once_with(['docker', 'push',
                                               f'{image_section.registry}/{image_section.name}:latest'])
    assert result.exit_code == 0

def test_image_clean(runner, env, dock, mock_commands_run, image_section):
    result = runner.invoke(dock, ['image', 'clean', image_section.section], env=env)
    mock_commands_run.assert_called_once_with(['docker', 'rmi', '--force',
                                               f'{image_section.registry}/{image_section.name}:latest'])
    assert result.exit_code == 0

def test_image_config(runner, env, dock, mock_update_config):
    result = runner.invoke(dock, ['image', 'config'], env=env)
    mock_update_config.assert_not_called()
    assert result.exit_code == 0
    assert result.output != ''

def test_image_config_init(runner, env, dock, mock_update_config):
    result = runner.invoke(dock, ['image', 'config', 'init', '--registry', 'mew'], env=env)
    mock_update_config.assert_called_once()
    assert result.exit_code == 0
    assert result.output != ''

def test_image_config_add(runner, env, dock, mock_update_config, valid_image_section, config_file):
    # pylint: disable=too-many-arguments
    path = str(config_file.parent / valid_image_section.section)
    result = runner.invoke(dock, ['image', 'config', 'add', path], env=env)
    mock_update_config.assert_called_once()
    assert result.exit_code == 0
    assert result.output != ''

def test_image_config_add_error(runner, env, dock, mock_update_config, invalid_image_section, config_file):
    # pylint: disable=too-many-arguments
    path = str(config_file.parent / invalid_image_section.section)
    result = runner.invoke(dock, ['image', 'config', 'add', path], env=env)
    mock_update_config.assert_not_called()
    assert result.exit_code == 2
