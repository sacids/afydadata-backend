from surveys.models import Survey, SurveyQuestions, SurveyResponses
from django import forms
from projects.models import Project


class ProjectForm(forms.ModelForm):
    """
    A class to create form
    """
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)


    class Meta:
        model  = Project
        fields  = ['title', 'description']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border-1 border-gray-200 rounded-none p-2 mb-3 my-1 focus:outline-none focus:border-1 focus:border-blue-200 focus:bg-white text-sm font-normal', 'id': 'title', 'placeholder': 'Write project title...', 'required': '' }),
            'description': forms.Textarea(attrs={'class': 'w-full bg-white text-gray-600 border-1 border-gray-200 rounded-none p-2 mb-3 my-1 focus:outline-none focus:border-1  focus:border-blue-200 focus:bg-white text-sm font-normal', 'id': 'description', 'placeholder': 'Write description...', 'rows': '3' }),
        } 

        labels = {
            'title': 'Project Title',
            'description': 'Description',
        } 


class SurveyForm(forms.ModelForm):
    """
    A class to create form
    """
    def __init__(self, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)


    class Meta:
        model  = Survey
        fields  = ['title', 'description', 'xform']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border-1 border-gray-200 rounded-none p-2 mb-3 my-1 focus:outline-none focus:border-1 focus:border-blue-200 focus:bg-white text-sm font-normal', 'id': 'title', 'placeholder': 'Write project title...', 'required': '' }),
            'xform': forms.FileInput(attrs={'class': 'w-full bg-white text-gray-600 border-1 border-gray-200 rounded-none p-2 mb-3 my-1 focus:outline-none focus:border-1 focus:border-blue-200 focus:bg-white text-sm font-normal'}),
            'description': forms.Textarea(attrs={'class': 'w-full bg-white text-gray-600 border-1 border-gray-200 rounded-none p-2 mb-3 my-1 focus:outline-none focus:border-1  focus:border-blue-200 focus:bg-white text-sm font-normal', 'id': 'description', 'placeholder': 'Write description...', 'rows': '3' }),
        } 

        labels = {
            'title': 'Form Title',
            'xform': 'Xform',
            'description': 'Description',
        }   

class UpdateMappingForm(forms.ModelForm):
    class Meta:
        model   = SurveyQuestions
        fields  = ['ref', 'col_name', 'label', 'hint', 'order','page']
        
    ref         = forms.CharField(disabled=True)
    col_name    = forms.CharField(disabled=True)
    hint        = forms.Textarea(attrs={'rows': 3})