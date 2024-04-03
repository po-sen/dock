import dataclasses
from click.testing import CliRunner

@dataclasses.dataclass()
class ChartSection():
    section: str
    name: str
    version: str = '0.1.0'
    registry: str = 'oci://registry-1.docker.io/namespace'

@dataclasses.dataclass()
class ImageSection():
    section: str
    name: str
    registry: str = 'namespace'

def invoke_cli(cli, args=None, env=None, catch_exceptions=True, color=False, expected_exit_code=0):
    # pylint: disable=too-many-arguments
    args = [] if args is None else args
    env = {} if env is None else env
    runner = CliRunner()
    result = runner.invoke(cli=cli, args=args, env=env, catch_exceptions=catch_exceptions, color=color)
    assert result.exit_code == expected_exit_code, (
        f"\n$ {''.join(f'{key}={value} ' for key, value in env.items())}dock {' '.join(args)}"
        f"\n{result.output}"
        f"\nExpected exit code {expected_exit_code} but got {result.exc_info[0].__name__}({result.exit_code})")
    return result.output
