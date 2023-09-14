from surveys.models import Survey, SurveyQuestions, SurveyResponses
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from projects.models import Project


class LoginForm(forms.Form):
    """Login form"""
    tailwind_class = """w-full bg-white text-gray-600 
    border border-gray-200 rounded-md px-2.5 py-2.5 mb-3 focus:outline-none 
    focus:border focus:border-blue-200 focus:bg-white text-sm font-normal"
    """

    username = forms.CharField(max_length=30, required=True, label=False, widget=forms.TextInput(
        attrs={'class': tailwind_class, 'placeholder': 'Write username...'}))
    password = forms.CharField(max_length=20, required=True, label=False, widget=forms.PasswordInput(
        attrs={'class': tailwind_class, 'placeholder': 'Password...'}))

    class Meta:
        fields = ('username', 'password')


class ChangePasswordForm(PasswordChangeForm):
    """Change password form"""
    old_password = forms.CharField(max_length=30, required=True, label="Old Password ", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Write old password...'}))
    new_password1 = forms.CharField(max_length=30, required=True, label="New Password ", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'New password...'}))
    new_password2 = forms.CharField(max_length=30, required=True, label="Confirm Password ", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm new password...'}))

    class Meta:
        fields = ('old_password', 'new_password1', 'new_password2')


class ProjectForm(forms.ModelForm):
    """
    A class to create form
    """

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Project
        fields = ['title', 'description']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border-1 border-gray-200 rounded-none p-2 mb-3 my-1 focus:outline-none focus:border-1 focus:border-blue-200 focus:bg-white text-sm font-normal', 'id': 'title', 'placeholder': 'Write project title...', 'required': ''}),
            'description': forms.Textarea(attrs={'class': 'w-full bg-white text-gray-600 border-1 border-gray-200 rounded-none p-2 mb-3 my-1 focus:outline-none focus:border-1  focus:border-blue-200 focus:bg-white text-sm font-normal', 'id': 'description', 'placeholder': 'Write description...', 'rows': '3'}),
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
        model = Survey
        fields = ['title', 'description', 'xform']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border-1 border-gray-200 rounded-none p-2 mb-3 my-1 focus:outline-none focus:border-1 focus:border-blue-200 focus:bg-white text-sm font-normal', 'id': 'title', 'placeholder': 'Write project title...', 'required': ''}),
            'xform': forms.FileInput(attrs={'class': 'w-full bg-white text-gray-600 border-1 border-gray-200 rounded-none p-2 mb-3 my-1 focus:outline-none focus:border-1 focus:border-blue-200 focus:bg-white text-sm font-normal'}),
            'description': forms.Textarea(attrs={'class': 'w-full bg-white text-gray-600 border-1 border-gray-200 rounded-none p-2 mb-3 my-1 focus:outline-none focus:border-1  focus:border-blue-200 focus:bg-white text-sm font-normal', 'id': 'description', 'placeholder': 'Write description...', 'rows': '3'}),
        }

        labels = {
            'title': 'Form Title',
            'xform': 'Xform',
            'description': 'Description',
        }


class UpdateMappingForm(forms.ModelForm):
    class Meta:
        model = SurveyQuestions
        fields = ['ref', 'col_name', 'label', 'hint', 'order', 'page']

    ref = forms.CharField(disabled=True)
    col_name = forms.CharField(disabled=True)
    hint = forms.Textarea(attrs={'rows': 3})
