from dataclasses import fields
from django.forms.widgets import Textarea
import datetime
from datetime import timedelta
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(forms.Form):
    """
    A class for profile
    """
    tailwind_class = """w-full bg-white text-gray-600 
    border border-gray-200 rounded-sm px-2.5 py-2.5 mb-3 focus:outline-none 
    focus:border focus:border-blue-200 focus:bg-white text-sm font-normal"
    """

    first_name = forms.CharField(max_length=30, required=True, label="Firstname ", widget=forms.TextInput(attrs={'class': tailwind_class, 'placeholder': 'Write first name...'}))
    last_name = forms.CharField(max_length=30, required=True, label="Lastname ", widget=forms.TextInput(attrs={'class': tailwind_class, 'placeholder': 'Write surname...'}))
    username = forms.CharField(max_length=30, required=True, label="Username ", widget=forms.TextInput(attrs={'class': tailwind_class, 'placeholder': 'Write username...'}))
    email = forms.EmailField(max_length=50, required=True, label="Email ", widget=forms.EmailInput(attrs={'class': tailwind_class, 'placeholder': 'Write email...'}))
    gender = forms.CharField(max_length=200, required=False, label="Gender ", widget=forms.TextInput(attrs={'class': tailwind_class}))
    pic = forms.ImageField(required=False, label="Profile Photo ", widget=forms.FileInput(attrs={'class': tailwind_class}))
    location = forms.CharField(max_length=200, required=False, label="Location ", widget=forms.TextInput(attrs={'class': tailwind_class, 'placeholder': 'Write location...'}))

    class Meta:
        fields = ('first_name', 'last_name', 'email', 'username', 'gender', 'pic', 'location' )


class ChangePasswordForm(PasswordChangeForm):
    """Change password form"""
    tailwind_class = """w-full bg-white text-gray-600 
    border border-gray-200 rounded-sm px-2.5 py-2.5 mb-3 focus:outline-none 
    focus:border focus:border-blue-200 focus:bg-white text-sm font-normal"
    """

    old_password = forms.CharField(max_length=30, required=True, label="Old Password ", widget=forms.PasswordInput(attrs={'class': tailwind_class, 'placeholder': 'Write old password...'}))
    new_password1 = forms.CharField(max_length=30, required=True, label="New Password ", widget=forms.PasswordInput(attrs={'class': tailwind_class, 'placeholder': 'New password...'}))
    new_password2 = forms.CharField(max_length=30, required=True, label="Confirm Password ", widget=forms.PasswordInput(attrs={'class': tailwind_class, 'placeholder': 'Confirm new password...'}))

    class Meta: 
        fields = ('old_password', 'new_password1', 'new_password2')


class UserForm(UserCreationForm):
    """User Form"""
    tailwind_class = """w-full bg-white text-gray-600 
    border border-gray-200 rounded-sm px-2.5 py-2.5 mb-3 focus:outline-none 
    focus:border focus:border-blue-200 focus:bg-white text-sm font-normal"
    """

    first_name = forms.CharField(max_length=50, label="First Name ", widget=forms.TextInput(attrs={'class': tailwind_class, 'placeholder': 'Write first name...'}))
    last_name = forms.CharField(max_length=50, label="Last Name ", widget=forms.TextInput(attrs={'class': tailwind_class, 'placeholder': 'Write surname...'}))
    username = forms.CharField(max_length=100, label="Username ", widget=forms.TextInput(attrs={'class': tailwind_class, 'placeholder': 'Write username...'}))
    email = forms.EmailField(max_length=100, label="Email ", widget=forms.EmailInput(attrs={'class': tailwind_class, 'placeholder': 'Write email...'}))
    password1 = forms.CharField(max_length=20, label="Password ", widget=forms.PasswordInput(attrs={'class': tailwind_class, 'placeholder': 'Password...'}))
    password2 = forms.CharField(max_length=20, label="Confirm Password ", widget=forms.PasswordInput(attrs={'class': tailwind_class, 'placeholder': 'Confirm password...'}))

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['username'].required = True
        self.fields['email'].required = True
        self.fields['password1'].required = True
        self.fields['password2'].required = True

        if self.instance.pk:
            self.fields['username'].required = False
            self.fields['email'].required = False
            self.fields['password1'].required = False
            self.fields['password2'].required = False

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2',)


class UserUpdateForm(UserChangeForm):
    """User Form"""
    tailwind_class = """w-full bg-white text-gray-600 
    border border-gray-200 rounded-sm px-2.5 py-2.5 mb-3 focus:outline-none 
    focus:border focus:border-blue-200 focus:bg-white text-sm font-normal"
    """

    first_name = forms.CharField(max_length=50, label="First Name", widget=forms.TextInput(attrs={'class': tailwind_class, 'placeholder': 'Write first name...'}))
    last_name = forms.CharField(max_length=50, label="Last Name", widget=forms.TextInput(attrs={'class': tailwind_class, 'placeholder': 'Write surname...'}))
    username = forms.CharField(max_length=100, label="Username", widget=forms.TextInput(attrs={'class': tailwind_class, 'placeholder': 'Write username...'}))
    email = forms.EmailField(max_length=100, label="Email", widget=forms.EmailInput(attrs={'class': tailwind_class, 'placeholder': 'Write email...'}))

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['username'].required = True
        self.fields['email'].required = True

        if self.instance.pk:
            self.fields['username'].required = False
            self.fields['email'].required = True

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username',)


class UserProfileForm(forms.ModelForm):        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Profile
        fields = ('gender', 'pic', 'location')

        tailwind_class = """w-full bg-white text-gray-600 
        border border-gray-200 rounded-sm px-2.5 py-2.5 mb-3 focus:outline-none 
        focus:border focus:border-blue-200 focus:bg-white text-sm font-normal"
        """

        widgets = {
            'gender': forms.Select(attrs={'class': tailwind_class, 'id': 'gender' }),
            'pic': forms.FileInput(attrs={'class': tailwind_class, 'id': 'pic' }),
            'location': forms.TextInput(attrs={'class': tailwind_class, 'id': 'location', 'placeholder': 'Write location...' }),
        }

        labels = {
            'gender': 'Gender ',
            'pic': 'Profile Photo ',
            'location': 'Location ',
        }
