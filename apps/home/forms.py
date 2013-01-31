from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from crispy_forms.bootstrap import InlineRadios
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))

class STEForm(forms.Form):
    STE_LIST = (
        ('1', 'AOS'),
        ('2', 'AOS2'),
        ('3', 'TFINT'),
        ('4', 'TFSD'),
        ('4', 'TFOHG'),
        ('5', 'VENDOR')
        )
    ste = forms.ChoiceField(widget=forms.RadioSelect, choices=STE_LIST, label='')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.form_tag = False

        self.helper.layout = Layout(
            Field('ste', template='layout/radio.html')
#            InlineRadios('ste')
            )

        super(STEForm, self).__init__(*args, **kwargs)
