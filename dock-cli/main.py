import configparser
import logging
import types
import click
import utils.helpers as hlp
from cli.chart import cli as chart_cli
from cli.image import cli as image_cli

CONTEXT_SETTINGS = {
    'help_option_names': ['-h', '--help'],
    'auto_envvar_prefix': 'DOCK',
}

@click.group(context_settings=CONTEXT_SETTINGS, cls=hlp.OrderedGroup)
@click.pass_context
@click.option('--docker',
              type=click.Path(exists=True, dir_okay=False, executable=True, resolve_path=True),
              help='Path to the Docker command.')
@click.option('--helm',
              type=click.Path(exists=True, dir_okay=False, executable=True, resolve_path=True),
              help='Path to the Helm command.')
@click.option('--git',
              type=click.Path(exists=True, dir_okay=False, executable=True, resolve_path=True),
              help='Path to the Git command.')
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
@click.version_option(package_name='dock-cli')
def cli(ctx, docker, helm, git, config_file, log_level):
    # pylint: disable=too-many-arguments
    logging.basicConfig(level=getattr(logging, log_level.upper()),
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s - %(levelname)s - %(name)s - "%(message)s"')

    ctx.obj = ctx.ensure_object(types.SimpleNamespace)

    command = hlp.Command()
    command.docker = command.docker if docker is None else docker
    command.helm = command.helm if helm is None else helm
    command.git = command.git if git is None else git
    ctx.obj.command = command

    logging.getLogger(__name__).debug('Reading configuration from %s', config_file)
    ctx.obj.config = configparser.ConfigParser()
    ctx.obj.config.read(config_file)
    ctx.obj.config_file = config_file

cli.add_command(chart_cli)
cli.add_command(image_cli)

if __name__ == '__main__':
    cli()
