import configparser
import logging
import types
import click

@click.group()
@click.pass_context
@click.option('-l', '--log-level',
              type=click.Choice(['debug', 'info', 'warning', 'error', 'fatal'], case_sensitive=False),
              default='info',
              show_default=True,
              help='Set the logging level')
@click.option('-c', '--config',
              type=click.Path(exists=False, dir_okay=False, readable=True, writable=True, resolve_path=True),
              default='dock.ini',
              show_default=True)
def cli(ctx, log_level, config):
    logging.basicConfig(level=getattr(logging, log_level.upper()),
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s - %(levelname)s - %(name)s - "%(message)s"')

    ctx.obj = ctx.ensure_object(types.SimpleNamespace)
    ctx.obj.config = configparser.ConfigParser()
    logging.getLogger(__name__).debug('Reading configuration from %s', config)
    ctx.obj.config.read(config)

    @ctx.call_on_close
    def update_config():
        logging.getLogger(__name__).debug('Updating configuration to %s', config)
        with open(config, 'w', encoding='utf-8') as fp:
            ctx.obj.config.write(fp)

@cli.command(name='ping')
def ping():
    click.echo('pong')

if __name__ == '__main__':
    cli()
