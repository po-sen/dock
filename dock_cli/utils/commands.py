import functools
import logging
import subprocess

def _validate_args(func, /):
    @functools.wraps(func)
    def wrapper(args):
        if not isinstance(args, list):
            raise TypeError('Expected args to be a list')
        valid_args = [str(arg) for arg in args if arg is not None]
        logging.getLogger(__name__).debug('Running command: `%s`', ' '.join(valid_args))
        return func(valid_args)
    return wrapper

@_validate_args
def run(args):
    subprocess.run(args, check=True)

@_validate_args
def getoutput(args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout.strip()
