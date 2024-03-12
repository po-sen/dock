import configparser
import logging
import types
import click
import utils.helpers as hlp
from chart import cli as chart
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
    commands = [('docker', docker),
                ('helm', helm),
                ('git', git)]
    ctx.obj.command = hlp.Command(**{k: v for k, v in commands if v is not None})
    ctx.obj.config_file = config_file

    logging.getLogger(__name__).debug('Reading configuration from %s', config_file)
    ctx.obj.config = configparser.ConfigParser()
    ctx.obj.config.read(config_file)

    @ctx.call_on_close
    def update_config():
        logging.getLogger(__name__).debug('Updating configuration to %s', config_file)
        with open(config_file, 'w', encoding='utf-8') as fp:
            ctx.obj.config.write(fp)

@cli.command(name='ping')
def ping():
    click.echo('pong')

cli.add_command(chart)
cli.add_command(image)

if __name__ == '__main__':
    cli()
