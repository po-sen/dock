from dock_cli.utils.utils import to_section

def validate_section(ctx, _param, value):
    if isinstance(value, tuple):
        for section in value:
            ctx.obj.helper.validate_section(section)
    if isinstance(value, str):
        ctx.obj.helper.validate_section(value)
    return value

def transform_to_section(_ctx, _param, value):
    if isinstance(value, tuple):
        return tuple(map(to_section, value))
    if isinstance(value, str):
        return to_section(value)
    return value

def multiline_values(_ctx, _param, value):
    if isinstance(value, tuple) and value:
        return '\n' + '\n'.join(value)
    return value

def multiline_sections(ctx, param, value):
    return multiline_values(ctx, param, transform_to_section(ctx, param, value))
