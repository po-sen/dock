import itertools
import click
import utils.commands as cmd
import utils.helpers as hlp

@click.group(name='image')
@click.pass_obj
def cli(obj):
    """Manage images

    This is a command line interface for manage images
    """
    obj.helper = hlp.ImageHelper(obj.config, obj.config_file)

@cli.command(name='list',
             help='List all images')
@click.pass_obj
def image_list(obj):
    for section in obj.helper.get_images():
        click.echo(section)

@cli.command(name='diff',
             help='List all images that have been changed between commits')
@click.pass_obj
@click.argument('commit1', nargs=1, required=False, type=str, default='HEAD')
@click.argument('commit2', nargs=1, required=False, type=str)
def image_diff(obj, commit1, commit2):
    for section in obj.helper.get_updated_images(obj.git, commit1, commit2):
        click.echo(section)

@cli.command(name='show',
             help='Show detailed information about a specific image')
@click.pass_obj
@click.argument('section', required=True, type=str)
@click.argument('tag', required=False, nargs=1, type=str, default='latest')
def image_show(obj, section, tag):
    click.echo(obj.helper.get_image_name(section, tag))

@cli.command(name='build',
             help='Build images')
@click.pass_obj
@click.argument('sections', nargs=-1, required=True, type=str)
@click.option('--tag', 'tags', multiple=True, type=str, default=['latest'])
def image_build(obj, sections, tags):
    for section in sections:
        cmd.run([obj.docker, 'build', obj.helper.get_section_path(section),
                 '--file', obj.helper.get_section_file(section),
                 *itertools.chain(*[('--tag', obj.helper.get_image_name(section, tag)) for tag in tags])])

@cli.command(name='push',
             help='Push images')
@click.pass_obj
@click.argument('sections', nargs=-1, required=True, type=str)
@click.option('--tag', 'tags', multiple=True, type=str, default=['latest'])
def image_push(obj, sections, tags):
    for section in sections:
        for tag in tags:
            cmd.run([obj.docker, 'push', obj.helper.get_image_name(section, tag)])

@cli.command(name='clean',
             help='Clean images')
@click.pass_obj
@click.argument('sections', nargs=-1, required=True, type=str)
@click.option('--tag', 'tags', multiple=True, type=str, default=['latest'])
def image_clean(obj, sections, tags):
    for section in sections:
        for tag in tags:
            cmd.run([obj.docker, 'rmi', '--force', obj.helper.get_image_name(section, tag)])
