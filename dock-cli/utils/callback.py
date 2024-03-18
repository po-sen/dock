import pathlib

def section_name(_ctx, _param, value):
    if isinstance(value, tuple):
        return tuple(pathlib.Path(section).as_posix() for section in value)
    return None if not value else pathlib.Path(value).as_posix()

def multiline_values(_ctx, _param, value):
    return None if not value else '\n' + '\n'.join(value)
