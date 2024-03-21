import configparser
import click
from dock_cli.utils import callback as cb
from dock_cli.utils import commands as cmd
from dock_cli.utils import helpers as hlp
from dock_cli.utils.schema import ChartConfigOptions as Chart, SectionType
from dock_cli.utils.utils import update_config, set_config_option, print_dock_config

@click.group(name='chart', cls=hlp.OrderedGroup)
@click.pass_obj
def cli(obj):
    """Manage charts

    This is a command line interface for manage charts
    """
    obj.helper = hlp.ChartHelper(obj.config, obj.config_file, obj.command)

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
@click.argument('section', required=True, type=click.Path(exists=True, file_okay=False), callback=cb.section_name)
def chart_show(obj, section):
    click.echo(obj.helper.get_chart(section))

@cli.command(name='package',
             help='Package charts')
@click.pass_obj
@click.argument('sections', nargs=-1, required=True,
                type=click.Path(exists=True, file_okay=False), callback=cb.section_name)
@click.option('--destination', required=False, type=click.Path(file_okay=False, writable=True), default='.')
def chart_package(obj, sections, destination):
    for section in sections:
        cmd.run([obj.command.helm, 'package', obj.helper.get_section_path(section), '--destination', destination])

@cli.command(name='push',
             help='Push charts')
@click.pass_obj
@click.argument('sections', nargs=-1, required=True,
                type=click.Path(exists=True, file_okay=False), callback=cb.section_name)
@click.option('--destination', required=False, type=click.Path(file_okay=False, writable=True), default='.')
def chart_push(obj, sections, destination):
    for section in sections:
        cmd.run([obj.command.helm, 'push',
                 obj.helper.get_chart_archive_file(section, destination),
                 obj.helper.get_section_registry(section)])

@cli.group(name='config', invoke_without_command=True, cls=hlp.OrderedGroup)
@click.pass_context
def config_cli(ctx):
    """Manage charts' configuration

    This is a command line interface for manage charts' configuration
    """
    if ctx.invoked_subcommand is None:
        for section in ctx.obj.helper.get_charts():
            print_dock_config(section, Chart)
        ctx.call_on_close(update_config)

@config_cli.command(name='init',
                    help='Initialize chart default settings in the configuration')
@click.pass_context
@click.option('--registry', required=False, type=str, default='oci://registry-1.docker.io/namespace')
@click.option('--file', required=False, type=str, default='Chart.yaml')
def config_init(ctx, registry, file):
    set_config_option(configparser.DEFAULTSECT, Chart.REGISTRY, registry)
    set_config_option(configparser.DEFAULTSECT, Chart.FILE, file)
    for section in ctx.obj.helper.get_charts():
        print_dock_config(section, Chart)
    ctx.call_on_close(update_config)

@config_cli.command(name='set',
                    help='Add or update an chart section in the configuration')
@click.pass_context
@click.argument('section', required=True, type=click.Path(exists=True, file_okay=False), callback=cb.section_name)
@click.option('--registry', required=False, type=str)
@click.option('--file', required=False, type=str)
def config_set(ctx, section, registry, file):
    if ctx.obj.config.has_section(section) is False:
        ctx.obj.config.add_section(section)
    set_config_option(section, Chart.REGISTRY, registry)
    set_config_option(section, Chart.FILE, file)
    set_config_option(section, Chart.TYPE, SectionType.CHART)
    ctx.obj.helper.validate_section(section)
    print_dock_config(section, Chart)
    ctx.call_on_close(update_config)
