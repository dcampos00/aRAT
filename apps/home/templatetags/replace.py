from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()

@register.filter
@stringfilter
def replace_by_space(value, arg):
    """
    function that replace the value in arg by a single space
    
    Arguments:
    `value`: original value
    `arg`: value to be replaced
    """
    return value.replace(arg, ' ')
