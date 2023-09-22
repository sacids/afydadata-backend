from surveys.models import Survey, SurveyQuestions, SurveyResponses
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from projects.models import Project, ProjectGroup, ProjectMember
from accounts.models import Profile


class LoginForm(forms.Form):
    """Login form"""
    tailwind_class = """w-full bg-white text-gray-600 
    border border-gray-200 rounded-none px-2.5 py-2.5 mb-3 focus:outline-none 
    focus:border focus:border-blue-200 focus:bg-white text-sm font-normal"
    """

    username = forms.CharField(max_length=30, required=True, label=False, widget=forms.TextInput(
        attrs={'class': tailwind_class, 'placeholder': 'Write username...'}))
    password = forms.CharField(max_length=20, required=True, label=False, widget=forms.PasswordInput(
        attrs={'class': tailwind_class, 'placeholder': 'Password...'}))

    class Meta:
        fields = ('username', 'password')


class ChangePasswordForm(forms.Form):
    """Change password form"""
    old_password = forms.CharField(max_length=30, required=True, label="Old Password ", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Write old password...'}))
    new_password1 = forms.CharField(max_length=30, required=True, label="New Password ", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'New password...'}))
    new_password2 = forms.CharField(max_length=30, required=True, label="Confirm Password ", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm new password...'}))

    class Meta:
        fields = ('old_password', 'new_password1', 'new_password2')


class ChangePmPasswordForm(forms.Form):
    """Change password form"""
    
    new_password1 = forms.CharField(max_length=30, required=True, label="New Password ", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'New password...'}))
    new_password2 = forms.CharField(max_length=30, required=True, label="Confirm Password ", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm new password...'}))

    class Meta:
        fields = ('new_password1', 'new_password2')

class ProjectForm(forms.ModelForm):
    """A class to create form"""
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

    class Meta:
        tailwind_class = """w-full bg-white text-gray-600 
        border border-gray-200 rounded-none px-2 py-2 mb-3 focus:outline-none 
        focus:border focus:border-blue-200 focus:bg-white text-sm font-normal"
        """
        model = Project
        fields = ['title', 'description']

        widgets = {
            'title': forms.TextInput(attrs={'class': tailwind_class, 'id': 'title', 'placeholder': 'Write project title...', 'required': ''}),
            'description': forms.Textarea(attrs={'class': tailwind_class, 'id': 'description', 'placeholder': 'Write description...', 'rows': '3'}),
        }

        labels = {
            'title': 'Title ',
            'description': 'Description ',
        }


class SurveyForm(forms.ModelForm):
    """
    A class to create form
    """

    def __init__(self, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)

    class Meta:
        tailwind_class = """w-full bg-white text-gray-600 
        border border-gray-200 rounded-none px-2 py-2 mb-3 focus:outline-none 
        focus:border focus:border-blue-200 focus:bg-white text-sm font-normal
        """

        model = Survey
        fields = ['title', 'description', 'xform']

        widgets = {
            'title': forms.TextInput(attrs={'class': tailwind_class, 'id': 'title', 'placeholder': 'Write project title...', 'required': ''}),
            'xform': forms.FileInput(attrs={'class': tailwind_class}),
            'description': forms.Textarea(attrs={'class': tailwind_class, 'id': 'description', 'placeholder': 'Write description...', 'rows': '3'}),
        }

        labels = {
            'title': 'Form Title ',
            'xform': 'Xform ',
            'description': 'Description ',
        }


class UpdateMappingForm(forms.ModelForm):
    class Meta:
        model = SurveyQuestions
        fields = ['ref', 'col_name', 'label', 'hint', 'order', 'page']

    ref = forms.CharField(disabled=True)
    col_name = forms.CharField(disabled=True)
    hint = forms.Textarea(attrs={'rows': 3})


class GroupForm(forms.ModelForm):
    
    """A class to create form"""
    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)

    class Meta:
        tailwind_class = """w-full bg-white text-gray-600 
        border border-gray-200 rounded-none px-2 py-2 mb-3 focus:outline-none 
        focus:border focus:border-blue-200 focus:bg-white text-sm font-normal"
        """
        model = ProjectGroup
        fields = ['title','description','project']
        
        widgets = {
          'project': forms.HiddenInput(),
          'description': forms.Textarea(attrs={'rows':3}),
        }
    
   

class MemberForm(forms.ModelForm):
    """A class to create form"""
    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)

    class Meta:
        tailwind_class = """w-full bg-white text-gray-600 
        border border-gray-200 rounded-none px-2 py-2 mb-3 focus:outline-none 
        focus:border focus:border-blue-200 focus:bg-white text-sm font-normal"
        """
        model = ProjectMember
        fields = ['member', 'projectGroup','project']
        
        widgets = {
            'project': forms.HiddenInput(),
            'projectGroup': forms.CheckboxSelectMultiple,
        }
        
        labels = {
            'member': 'Member ',
            'projectGroup': 'Group ',
        }

class ManageMemberGroupsFrom(forms.ModelForm):
    """A class to create form"""
    def __init__(self, *args, **kwargs):
        super(ManageMemberGroupsFrom, self).__init__(*args, **kwargs)

    class Meta:
        tailwind_class = """w-full bg-white text-gray-600 
        border border-gray-200 rounded-none px-2 py-2 mb-3 focus:outline-none 
        focus:border focus:border-blue-200 focus:bg-white text-sm font-normal"
        """
        model = ProjectMember
        fields = ['projectGroup']
        
        widgets = {
            'projectGroup': forms.CheckboxSelectMultiple,
        }
        
        labels = {
            'projectGroup': 'Group ',
        }

    