def test_dock(runner, dock):
    result = runner.invoke(dock)
    assert result.exit_code == 0

def test_dock_version_option(runner, dock):
    result = runner.invoke(dock, ['--version'])
    assert result.exit_code == 0

def test_dock_help_option(runner, dock, help_option):
    result = runner.invoke(dock, [help_option])
    assert result.exit_code == 0

def test_dock_chart(runner, dock):
    result = runner.invoke(dock, ['chart'])
    assert result.exit_code == 0

def test_dock_chart_help_option(runner, dock, help_option):
    result = runner.invoke(dock, ['chart', help_option])
    assert result.exit_code == 0

def test_dock_image(runner, dock):
    result = runner.invoke(dock, ['image'])
    assert result.exit_code == 0

def test_dock_image_help_option(runner, dock, help_option):
    result = runner.invoke(dock, ['image', help_option])
    assert result.exit_code == 0
