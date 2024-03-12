import click
import utils.commands as cmd
import utils.helpers as hlp

@click.group(name='chart')
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
@click.argument('section', required=True, type=str)
def chart_show(obj, section):
    click.echo(obj.helper.get_chart(section))

@cli.command(name='package',
             help='Package charts')
@click.pass_obj
@click.argument('sections', nargs=-1, required=True, type=str)
@click.option('--destination', required=False, type=click.Path(file_okay=False, writable=True), default='.')
def chart_package(obj, sections, destination):
    for section in sections:
        cmd.run([obj.command.helm, 'package', obj.helper.get_section_path(section), '--destination', destination])

@cli.command(name='push',
             help='Push charts')
@click.pass_obj
@click.argument('sections', nargs=-1, required=True, type=str)
@click.option('--destination', required=False, type=click.Path(file_okay=False, writable=True), default='.')
def chart_push(obj, sections, destination):
    for section in sections:
        cmd.run([obj.command.helm, 'push', obj.helper.get_chart_archive_file(section, destination)])
