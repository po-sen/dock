import configparser
import itertools
import click
from dock_cli.utils import callback as cb
from dock_cli.utils import commands as cmd
from dock_cli.utils import helpers as hlp
from dock_cli.utils import utils
from dock_cli.utils.schema import ImageConfigOptions as Image, SectionType

@click.group(name='image', cls=hlp.OrderedGroup)
@click.pass_obj
def cli(obj):
    """Manage images

    This is a command line interface for manage images
    """
    obj.helper = hlp.ImageHelper(obj.config, obj.config_dir, obj.command)

@cli.command(name='list',
             help='List all images')
@click.pass_obj
def image_list(obj):
    for section in obj.helper.get_images():
        click.echo(section)

@cli.command(name='diff',
             help='List all images that have been changed between commits')
@click.pass_obj
@click.argument('commit1', required=False, type=str, default='HEAD')
@click.argument('commit2', required=False, type=str)
def image_diff(obj, commit1, commit2):
    for section in obj.helper.get_updated_images(commit1, commit2):
        click.echo(section)

@cli.command(name='show',
             help='Show detailed information about a specific image')
@click.pass_obj
@click.argument('section', required=True, type=str, callback=cb.validate_section)
@click.argument('tag', required=False, type=str, default='latest')
def image_show(obj, section, tag):
    click.echo(obj.helper.get_image(section, tag))

@cli.command(name='build',
             help='Build images')
@click.pass_obj
@click.argument('sections', nargs=-1, required=True, type=str, callback=cb.validate_section)
@click.option('--tag', 'tags', multiple=True, type=str, default=['latest'], show_default=True,
              help='Specify one or multiple tags for the image')
def image_build(obj, sections, tags):
    for section in sections:
        cmd.run([obj.command.docker, 'build', obj.helper.get_section_path(section),
                 '--file', obj.helper.get_section_file(section),
                 *itertools.chain(*[('--tag', obj.helper.get_image(section, tag)) for tag in tags])])

@cli.command(name='push',
             help='Push images')
@click.pass_obj
@click.argument('sections', nargs=-1, required=True, type=str, callback=cb.validate_section)
@click.option('--tag', 'tags', multiple=True, type=str, default=['latest'], show_default=True,
              help='Specify one or multiple tags for the image')
def image_push(obj, sections, tags):
    for section in sections:
        for tag in tags:
            cmd.run([obj.command.docker, 'push', obj.helper.get_image(section, tag)])

@cli.command(name='clean',
             help='Clean images')
@click.pass_obj
@click.argument('sections', nargs=-1, required=True, type=str, callback=cb.validate_section)
@click.option('--tag', 'tags', multiple=True, type=str, default=['latest'], show_default=True,
              help='Specify one or multiple tags for the image')
def image_clean(obj, sections, tags):
    for section in sections:
        for tag in tags:
            cmd.run([obj.command.docker, 'rmi', '--force', obj.helper.get_image(section, tag)])

@cli.command(name='view',
             help="View current images' configuration")
@click.pass_obj
def config_view(obj):
    for section in obj.helper.get_images():
        utils.print_image_config(obj.config, section)

@cli.command(name='set-registry',
             help='Set default registry for all images in the configuration')
@click.pass_obj
@click.argument('registry', required=False, type=str, default='namespace')
@click.option('-y', '--assume-yes', is_flag=True, default=False, help='Update config without a prompt')
def config_set_registry(obj, registry, assume_yes):
    utils.set_config_option(obj.config, configparser.DEFAULTSECT, Image.REGISTRY, registry)
    utils.update_config(obj.config, obj.config_file, assume_yes)

@cli.command(name='set',
             help='Add or update an image section in the configuration')
@click.pass_obj
@click.argument('section', required=True, type=click.Path(exists=True, file_okay=False),
                callback=cb.transform_to_section)
@click.option('--image-file', required=False, type=str, default='Dockerfile', show_default=True,
              help='Name of the Dockerfile for this section.')
@click.option('--image-name', required=False, type=str,
              help='Name of the image for this section.')
@click.option('--depends-on', required=False, multiple=True,
              type=click.Path(exists=True),
              callback=cb.multiline_sections,
              help='List of sections or paths that this section depends on.')
@click.option('-y', '--assume-yes', is_flag=True, default=False, help='Update config without a prompt')
def config_set(obj, section, image_file, image_name, depends_on, assume_yes):
    # pylint: disable=too-many-arguments
    if not obj.config.get(configparser.DEFAULTSECT, Image.REGISTRY, fallback=''):
        registry = click.prompt('Enter default registry for all images',
                                default='namespace', type=str).strip()
        utils.set_config_option(obj.config, configparser.DEFAULTSECT, Image.REGISTRY, registry)
    utils.set_config_section(obj.config, section)
    utils.set_config_option(obj.config, section, Image.TYPE, SectionType.IMAGE)
    utils.set_config_option(obj.config, section, Image.FILE, image_file)
    utils.set_config_option(obj.config, section, Image.NAME, image_name)
    utils.set_config_option(obj.config, section, Image.DEPENDS_ON, depends_on)
    obj.helper.validate_section(section)
    utils.update_config(obj.config, obj.config_file, assume_yes)

@cli.command(name='unset',
             help='Remove an image section in the configuration')
@click.pass_obj
@click.argument('sections', nargs=-1, required=True, type=str, callback=cb.validate_section)
@click.option('-y', '--assume-yes', is_flag=True, default=False, help='Update config without a prompt')
def config_unset(obj, sections, assume_yes):
    # pylint: disable=duplicate-code
    for section in sections:
        utils.unset_config_section(obj.config, section)
    utils.update_config(obj.config, obj.config_file, assume_yes)
