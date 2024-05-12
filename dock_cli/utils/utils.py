import logging
import pathlib
import click
from dock_cli.utils.schema import ImageConfigOptions as Image, ChartConfigOptions as Chart

def update_config(config, config_file):
    if click.confirm('Do you want to update the configuration?'):
        logging.getLogger(__name__).debug('Updating configuration to %s', config_file)
        with open(config_file, 'w', encoding='utf-8') as fp:
            config.write(fp)
        click.echo('  Successfully updated.')
    else:
        click.echo('  Cancel the update.')

def to_section(config_dir, value):
    section = pathlib.Path(value).resolve().relative_to(config_dir).as_posix()
    logging.getLogger(__name__).debug("Transform value '%s' to section '%s'", value, section)
    return section

def set_config_option(config, section, option, value=None):
    logging.getLogger(__name__).debug("Removing section [%s] option '%s'", section, option)
    config.remove_option(section, option)
    if value:
        logging.getLogger(__name__).debug("Setting section [%s] option '%s' to '%s'", section, option, value)
        config.set(section, option, value)
        click.echo(f"  {click.style(f'Set [{section}] {option} = {value}', fg='green')}")
    else:
        click.echo(f"  {click.style(f'Set [{section}] {option} = ', fg='red')}")
        logging.getLogger(__name__).debug("Skipping section [%s] option '%s' because value was '%s'",
                                          section, option, value)

def set_config_section(config, section):
    logging.getLogger(__name__).debug('Setting section [%s]', section)
    if config.has_section(section) is False:
        config.add_section(section)
        click.echo(f"  {click.style(f'Set [{section}]', fg='green')}")

def unset_config_section(config, section):
    logging.getLogger(__name__).debug('Removing section [%s]', section)
    if config.has_section(section) is True:
        config.remove_section(section)
        click.echo(f"  {click.style(f'Unset [{section}]', fg='red')}")

def print_image_config(config, section):
    click.echo(f"{click.style(section, fg='bright_cyan')}:")
    for option in Image:
        value = ' '.join(config.get(section, option, fallback='').strip().splitlines())
        click.echo(f"- {click.style(option, fg='green')}: {click.style(value, fg='yellow')}")

def print_chart_config(config, section):
    click.echo(f"{click.style(section, fg='bright_cyan')}:")
    for option in Chart:
        value = ' '.join(config.get(section, option, fallback='').strip().splitlines())
        click.echo(f"- {click.style(option, fg='green')}: {click.style(value, fg='yellow')}")

def topological_sort(dependencies):
    visited = set()
    result = []

    def _dfs(node):
        if node in visited:
            return
        visited.add(node)
        for neighbor in dependencies[node]:
            if neighbor in dependencies:
                _dfs(neighbor)
        result.append(node)

    for node in dependencies:
        if node not in visited:
            _dfs(node)

    return result
