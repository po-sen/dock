import logging
import pathlib
import click
from dock_cli.utils.schema import ImageConfigOptions as Image, ChartConfigOptions as Chart

@click.pass_obj
def update_config(obj):
    logging.getLogger(__name__).debug('Updating configuration to %s', obj.config_file)
    with open(obj.config_file, 'w', encoding='utf-8') as fp:
        obj.config.write(fp)

@click.pass_obj
def to_section(obj, value):
    section = pathlib.Path(value).resolve().relative_to(obj.config_dir).as_posix()
    logging.getLogger(__name__).debug('Transform value `%s` to section `%s`', value, section)
    return section

@click.pass_obj
def set_config_option(obj, section, option, value=None):
    logging.getLogger(__name__).debug('Removing section [%s] option `%s`', section, option)
    obj.config.remove_option(section, option)
    if value:
        logging.getLogger(__name__).debug('Setting section [%s] option `%s` to `%s`', section, option, value)
        obj.config.set(section, option, value)
        click.echo(f'Set [{section}] {option} = {value}')

@click.pass_obj
def print_image_config(obj, section):
    click.echo(f"{click.style(section, fg='bright_cyan')}:")
    for option in Image:
        value = ' '.join(obj.config.get(section, option, fallback='').strip().splitlines())
        click.echo(f"- {click.style(option, fg='green')}: {click.style(value, fg='yellow')}")

@click.pass_obj
def print_chart_config(obj, section):
    click.echo(f"{click.style(section, fg='bright_cyan')}:")
    for option in Chart:
        value = ' '.join(obj.config.get(section, option, fallback='').strip().splitlines())
        click.echo(f"- {click.style(option, fg='green')}: {click.style(value, fg='yellow')}")

def topological_sort(dependencies):
    visited = set()
    result = []

    def dfs(node):
        if node in visited:
            return
        visited.add(node)
        for neighbor in dependencies[node]:
            if neighbor in dependencies:
                dfs(neighbor)
        result.append(node)

    for node in dependencies:
        if node not in visited:
            dfs(node)

    return result
