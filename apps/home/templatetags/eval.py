from django.template import Library

register = Library()

@register.tag(name='eval')
def do_eval(parser, token):
    """Usage: {% eval %}{% endeval %}"""

    nodelist = parser.parse(('endeval',))

    class EvalNode(template.Node):
        def render(self, context):
            return eval(nodelist.render(context))
 
    parser.delete_first_token()
    return EvalNode()

@register.filter(name='eval')
def eval_filter(value):
    return eval(value)
