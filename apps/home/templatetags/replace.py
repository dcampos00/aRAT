from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()


@register.filter
@stringfilter
def replace_by_space(value, arg):
    """
    Replace the all occurrences of arg in value by a single space

    Arguments:
    `value`: original string that will be replaced
    `arg`: value to be replaced by a single space
    """
    return value.replace(arg, ' ')
