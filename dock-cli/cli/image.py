import configparser
import itertools
import click
import utils.callback as cb
import utils.commands as cmd
import utils.helpers as hlp
from utils.schema import ImageConfigOptions as Image, SectionType
from utils.utils import update_config, set_config_option, print_dock_config

@click.group(name='image', cls=hlp.OrderedGroup)
@click.pass_obj
def cli(obj):
    """Manage images

    This is a command line interface for manage images
    """
    obj.helper = hlp.ImageHelper(obj.config, obj.config_file, obj.command)

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
@click.argument('section', required=True, type=click.Path(exists=True, file_okay=False), callback=cb.section_name)
@click.argument('tag', required=False, type=str, default='latest')
def image_show(obj, section, tag):
    click.echo(obj.helper.get_image(section, tag))

@cli.command(name='build',
             help='Build images')
@click.pass_obj
@click.argument('sections', nargs=-1, required=True,
                type=click.Path(exists=True, file_okay=False), callback=cb.section_name)
@click.option('--tag', 'tags', multiple=True, type=str, default=['latest'])
def image_build(obj, sections, tags):
    for section in sections:
        cmd.run([obj.command.docker, 'build', obj.helper.get_section_path(section),
                 '--file', obj.helper.get_section_file(section),
                 *itertools.chain(*[('--tag', obj.helper.get_image(section, tag)) for tag in tags])])

@cli.command(name='push',
             help='Push images')
@click.pass_obj
@click.argument('sections', nargs=-1, required=True,
                type=click.Path(exists=True, file_okay=False), callback=cb.section_name)
@click.option('--tag', 'tags', multiple=True, type=str, default=['latest'])
def image_push(obj, sections, tags):
    for section in sections:
        for tag in tags:
            cmd.run([obj.command.docker, 'push', obj.helper.get_image(section, tag)])

@cli.command(name='clean',
             help='Clean images')
@click.pass_obj
@click.argument('sections', nargs=-1, required=True,
                type=click.Path(exists=True, file_okay=False), callback=cb.section_name)
@click.option('--tag', 'tags', multiple=True, type=str, default=['latest'])
def image_clean(obj, sections, tags):
    for section in sections:
        for tag in tags:
            cmd.run([obj.command.docker, 'rmi', '--force', obj.helper.get_image(section, tag)])

@cli.group(name='config', invoke_without_command=True, cls=hlp.OrderedGroup)
@click.pass_context
def config_cli(ctx):
    """Manage images' configuration

    This is a command line interface for manage images' configuration
    """
    if ctx.invoked_subcommand is None:
        for section in ctx.obj.helper.get_images():
            print_dock_config(section, Image)
        ctx.call_on_close(update_config)

@config_cli.command(name='init',
                    help='Initialize image default settings in the configuration')
@click.pass_context
@click.option('--registry', required=False, type=str, default='namespace')
@click.option('--file', required=False, type=str, default='Dockerfile')
def config_init(ctx, registry, file):
    set_config_option(configparser.DEFAULTSECT, Image.REGISTRY, registry)
    set_config_option(configparser.DEFAULTSECT, Image.FILE, file)
    for section in ctx.obj.helper.get_images():
        print_dock_config(section, Image)
    ctx.call_on_close(update_config)

@config_cli.command(name='set',
                    help='Add or update an image section in the configuration')
@click.pass_context
@click.argument('section', required=True, type=click.Path(exists=True, file_okay=False), callback=cb.section_name)
@click.option('--registry', required=False, type=str)
@click.option('--file', required=False, type=str)
@click.option('--name', required=False, type=str)
@click.option('--depends-on', required=False, multiple=True,
              type=click.Path(exists=True, file_okay=False), callback=cb.multiline_section_name)
def config_set(ctx, section, registry, file, name, depends_on):
    # pylint: disable=too-many-arguments
    if ctx.obj.config.has_section(section) is False:
        ctx.obj.config.add_section(section)
    set_config_option(section, Image.REGISTRY, registry)
    set_config_option(section, Image.FILE, file)
    set_config_option(section, Image.NAME, name)
    set_config_option(section, Image.DEPENDS_ON, depends_on)
    set_config_option(section, Image.TYPE, SectionType.IMAGE)
    ctx.obj.helper.validate_section(section)
    print_dock_config(section, Image)
    ctx.call_on_close(update_config)
