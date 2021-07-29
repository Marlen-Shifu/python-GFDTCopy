from django import forms
from .models import Task

'''from django.forms.widgets import DateInput

class MyDateInput(DateInput):
    input_type = 'date'''


class TaskModelForm(forms.ModelForm):

    '''def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment'].widget.attributes.disable = True'''

    def clean(self):
        cleaned_data = self.cleaned_data
        user_email = cleaned_data['user_email']
        verificator_email = cleaned_data['verificator_email']

        if user_email == verificator_email:
            self.add_error(None, 'User email and verificator email can\'t be same')

    class Meta:
        model = Task
        exclude = ['verified', 'closed', 'paid']
