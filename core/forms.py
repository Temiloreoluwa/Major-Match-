from django import forms
from .models import Question

class QuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)
        for question in questions:
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=question.text,
                choices=[(True, 'Yes'), (False, 'No')],
                widget=forms.RadioSelect,
                required=True
            )
