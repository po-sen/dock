from helpers import invoke_cli

def test_dock(dock):
    invoke_cli(dock)

def test_dock_version_option(dock):
    invoke_cli(dock, ['--version'])

def test_dock_help_option(dock, help_option):
    invoke_cli(dock, [help_option])

def test_dock_chart(dock):
    invoke_cli(dock, ['chart'])

def test_dock_chart_help_option(dock, help_option):
    invoke_cli(dock, ['chart', help_option])

def test_dock_image(dock):
    invoke_cli(dock, ['image'])

def test_dock_image_help_option(dock, help_option):
    invoke_cli(dock, ['image', help_option])
