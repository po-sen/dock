import configparser
import click
from dock_cli.utils import callback as cb
from dock_cli.utils import commands as cmd
from dock_cli.utils import helpers as hlp
from dock_cli.utils import utils
from dock_cli.utils.schema import ChartConfigOptions as Chart, SectionType

@click.group(name='chart', cls=hlp.OrderedGroup)
@click.pass_obj
def cli(obj):
    """Manage charts

    This is a command line interface for manage charts
    """
    obj.helper = hlp.ChartHelper(obj.config, obj.config_dir, obj.command)

@cli.command(name='list',
             help='List all charts')
@click.pass_obj
def chart_list(obj):
    for section in obj.helper.get_charts():
        click.echo(section)

@cli.command(name='diff',
             help='List all charts that have been changed between commits')
@click.pass_obj
@click.argument('commit1', nargs=1, required=False, type=str, default='HEAD')
@click.argument('commit2', nargs=1, required=False, type=str)
def chart_diff(obj, commit1, commit2):
    for section in obj.helper.get_updated_charts(commit1, commit2):
        click.echo(section)

@cli.command(name='show',
             help='Show detailed information about a specific chart')
@click.pass_obj
@click.argument('section', required=True, type=str, callback=cb.validate_section)
def chart_show(obj, section):
    click.echo(obj.helper.get_chart(section))

@cli.command(name='package',
             help='Package charts')
@click.pass_obj
@click.argument('sections', nargs=-1, required=True, type=str, callback=cb.validate_section)
@click.option('--destination', required=False, type=click.Path(file_okay=False, writable=True), default='.')
def chart_package(obj, sections, destination):
    for section in sections:
        cmd.run([obj.command.helm, 'package', obj.helper.get_section_path(section), '--destination', destination])

@cli.command(name='push',
             help='Push charts')
@click.pass_obj
@click.argument('sections', nargs=-1, required=True, type=str, callback=cb.validate_section)
@click.option('--destination', required=False, type=click.Path(file_okay=False, writable=True), default='.')
def chart_push(obj, sections, destination):
    for section in sections:
        cmd.run([obj.command.helm, 'push',
                 obj.helper.get_chart_archive_file(section, destination),
                 obj.helper.get_section_registry(section)])

@cli.command(name='view',
             help="View current charts' configuration")
@click.pass_obj
def config_view(obj):
    for section in obj.helper.get_charts():
        utils.print_chart_config(obj.config, section)

@cli.command(name='set-registry',
             help='Set default registry for all charts in the configuration')
@click.pass_obj
@click.argument('registry', required=False, type=str, default='oci://registry-1.docker.io/namespace')
def config_set_registry(obj, registry):
    utils.set_config_option(obj.config, configparser.DEFAULTSECT, Chart.REGISTRY, registry)
    utils.update_config(obj.config, obj.config_file)

@cli.command(name='set',
             help='Add or update an chart section in the configuration')
@click.pass_obj
@click.argument('section', required=True, type=click.Path(exists=True, file_okay=False),
                callback=cb.transform_to_section)
def config_set(obj, section):
    if not obj.config.get(configparser.DEFAULTSECT, Chart.REGISTRY, fallback=''):
        registry = click.prompt('Enter default registry for all charts',
                                default='oci://registry-1.docker.io/namespace', type=str).strip()
        utils.set_config_option(obj.config, configparser.DEFAULTSECT, Chart.REGISTRY, registry)
    utils.set_config_section(obj.config, section)
    utils.set_config_option(obj.config, section, Chart.TYPE, SectionType.CHART)
    obj.helper.validate_section(section)
    utils.update_config(obj.config, obj.config_file)

@cli.command(name='unset',
             help='Remove an chart section in the configuration')
@click.pass_obj
@click.argument('sections', nargs=-1, required=True, type=str, callback=cb.validate_section)
def config_unset(obj, sections):
    # pylint: disable=duplicate-code
    for section in sections:
        utils.unset_config_section(obj.config, section)
    utils.update_config(obj.config, obj.config_file)
