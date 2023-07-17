from surveys.models import Survey, SurveyQuestions, SurveyResponses
from django import forms

class UpdateMappingForm(forms.ModelForm):
    class Meta:
        model   = SurveyQuestions
        fields  = ['ref', 'col_name', 'label', 'hint', 'order','page']
        
    ref         = forms.CharField(disabled=True)
    col_name    = forms.CharField(disabled=True)
    hint        = forms.Textarea(attrs={'rows': 3})