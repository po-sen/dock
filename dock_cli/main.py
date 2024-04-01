import configparser
import logging
import pathlib
import types
import click
from dock_cli.utils import helpers as hlp
from dock_cli.cli.chart import cli as chart_cli
from dock_cli.cli.image import cli as image_cli

CONTEXT_SETTINGS = {
    'help_option_names': ['-h', '--help'],
    'auto_envvar_prefix': 'DOCK',
}

@click.group(context_settings=CONTEXT_SETTINGS, cls=hlp.OrderedGroup,
             help='CLI tool for managing containerized applications in a Git repository')
@click.pass_context
@click.option('-c', '--config-file',
              type=click.Path(dir_okay=False, readable=True, writable=True, resolve_path=True),
              default='dock.ini',
              show_default=True,
              help='Path to the configuration file.')
@click.option('-l', '--log-level',
              type=click.Choice(['debug', 'info', 'warning', 'error', 'fatal'], case_sensitive=False),
              default='info',
              show_default=True,
              help='Set the logging level.')
@click.option('--docker',
              type=click.Path(exists=True, dir_okay=False, executable=True, resolve_path=True),
              help='Path to the Docker command.')
@click.option('--helm',
              type=click.Path(exists=True, dir_okay=False, executable=True, resolve_path=True),
              help='Path to the Helm command.')
@click.option('--git',
              type=click.Path(exists=True, dir_okay=False, executable=True, resolve_path=True),
              help='Path to the Git command.')
@click.version_option(package_name='dock-cli')
def cli(ctx, config_file, log_level, docker, helm, git):
    # pylint: disable=too-many-arguments
    logging.basicConfig(level=getattr(logging, log_level.upper()),
                        format='[%(levelname)s] %(message)s')

    ctx.ensure_object(types.SimpleNamespace)
    ctx.obj.command = hlp.Command(docker, helm, git)

    logging.getLogger(__name__).debug('Reading configuration from %s', config_file)
    ctx.obj.config = configparser.ConfigParser()
    ctx.obj.config.read(config_file)
    ctx.obj.config_dir = pathlib.Path(config_file).parent.as_posix()
    ctx.obj.config_file = config_file

cli.add_command(chart_cli)
cli.add_command(image_cli)

if __name__ == '__main__':
    cli()
