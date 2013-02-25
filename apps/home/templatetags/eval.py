from django.template import Library

register = Library()


@register.tag(name='eval')
def do_eval(parser, token):
    """
    Template Tag that allows evaluate the content inside itself

    Usage: {% eval %}{% endeval %}
    """

    nodelist = parser.parse(('endeval',))

    class EvalNode(template.Node):
        def render(self, context):
            return eval(nodelist.render(context))

    parser.delete_first_token()
    return EvalNode()


@register.filter(name='eval')
def eval_filter(value):
    """
    Template Filter that return the content evaluated of value

    Arguments:
    value -- string that will be evaluated

    Usage: {{ string_to_evaluate|eval }}
           {% for x in string_to_evaluate|eval %}
             ...
           {% endfor %}
    """
    return eval(value)
