from jinja2 import Environment, FileSystemLoader, meta
from jinja2.nodes import Assign, Filter, And, Or
from jinja2 import TemplateNotFound as JinjaTemplateNotFound
from src.exceptions import TemplateNotFound, MissingArguments


jinja_env = Environment(loader=FileSystemLoader("templates/"))


def find_optional_variables(parsed_content):
    variable_names = set()
    for element in parsed_content.body:
        if not isinstance(element, Assign):
            continue
        node, target_name = element.node, element.target.name
        if isinstance(node, Filter) and node.name == 'default' and node.node.name == target_name:
            variable_names.add(target_name)
        elif isinstance(node, And):
            variable_names.add(node.left.name)
        elif isinstance(node, Or) and node.left.name == target_name:
            variable_names.add(target_name)
    return variable_names


def render_template(template_name, **kwargs):
    try:
        template_source = jinja_env.loader.get_source(jinja_env, f'{template_name}.jinja')[0]
    except JinjaTemplateNotFound:
        raise TemplateNotFound(f'Template "{template_name}.jinja" not found in "templates".')
    template = jinja_env.from_string(template_source)
    parsed_content = jinja_env.parse(template_source)
    variables = meta.find_undeclared_variables(parsed_content)
    optionals = find_optional_variables(parsed_content)
    required = variables.difference(optionals)
    passed = set(kwargs.keys())
    not_passed = required.difference(passed)
    # ignored = variables.difference(passed)
    if not_passed:
        raise MissingArguments(f'Missing required arguments: {", ".join(list(sorted(not_passed)))}')
    return template.render(**kwargs)
