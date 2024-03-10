import configparser
import logging
import types
import click
from utils.constants import Command
from image import cli as image

CONTEXT_SETTINGS = {
    'help_option_names': ['-h', '--help'],
    'auto_envvar_prefix': 'DOCK',
}

@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
@click.option('--docker',
              type=click.Path(exists=True, dir_okay=False, executable=True, resolve_path=True),
              help='Path to the Docker command.')
@click.option('--git',
              type=click.Path(exists=True, dir_okay=False, executable=True, resolve_path=True),
              help='Path to the Git command.')
@click.option('-c', '--config',
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
def cli(ctx, docker, git, config, log_level):
    logging.basicConfig(level=getattr(logging, log_level.upper()),
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s - %(levelname)s - %(name)s - "%(message)s"')

    ctx.obj = ctx.ensure_object(types.SimpleNamespace)
    ctx.obj.docker = Command.DOCKER.value if docker is None else docker
    ctx.obj.git = Command.GIT.value if git is None else git
    ctx.obj.config_file = config

    logging.getLogger(__name__).debug('Reading configuration from %s', config)
    ctx.obj.config = configparser.ConfigParser()
    ctx.obj.config.read(config)

    @ctx.call_on_close
    def update_config():
        logging.getLogger(__name__).debug('Updating configuration to %s', config)
        with open(config, 'w', encoding='utf-8') as fp:
            ctx.obj.config.write(fp)

@cli.command(name='ping')
def ping():
    click.echo('pong')

cli.add_command(image)

if __name__ == '__main__':
    cli()
