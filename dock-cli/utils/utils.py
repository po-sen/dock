import logging
import click

@click.pass_obj
def update_config(obj):
    logging.getLogger(__name__).debug('Updating configuration to %s', obj.config_file)
    with open(obj.config_file, 'w', encoding='utf-8') as fp:
        obj.config.write(fp)

@click.pass_obj
def set_config_option(obj, section, option, value=None):
    logging.getLogger(__name__).debug('Removing section [%s] option `%s`', section, option)
    obj.config.remove_option(section, option)
    if value is not None:
        logging.getLogger(__name__).debug('Setting section [%s] option `%s` to `%s`', section, option, value)
        obj.config.set(section, option, value)
