import unicodedata

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from.models import Cluster, News,News_category, Action_flag,Modules, Activity_Log, Client, is_agency_represented, ContactJACK_message, Content_Manager
from tinymce.widgets import TinyMCE
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext, gettext_lazy as _

class NewUserForm(forms.ModelForm):
    username = forms.CharField(
        label="Username",
        help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.")
    )
    first_name = forms.CharField(label="Given Name")
    last_name = forms.CharField(label="Surname")
    email = forms.EmailField(label="Email address")
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email","password1","password2")


from .models import Candidate


# class CandidateForm(forms.ModelForm):
#
#     class Meta:
#         model = Candidate
#         fields = ['cluster','votes']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

class NewsForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=News_category.objects.all(), empty_label= "Select News Category")

    class Meta:
        model = News
        fields = ['category','headline','content','picture']
        labels = {'category':'lolwtf', 'headline':'Headline', 'content':'Content','picture':'Cover Image'}
        widgets = {
            'content': TinyMCE()
        }

class ClientForm(forms.ModelForm):
    is_agency_represented = forms.ModelChoiceField(queryset=is_agency_represented.objects.all(), empty_label= "Select Option", label='Is the brand represented by an agency? ')
    email = forms.EmailField(label="Email Address")

    class Meta:
        model = Client
        fields = '__all__'
        exclude = ['datetime', 'is_newsletter']
        labels = {'name':'Name',
                  'brand_name':'Brand Name',
                  'agency_name':'Agency Name (if applicable)',
                  'your_position':'Your Position',
                  'contact_number':'Contact Number',
                  'email':'Email',
                  'other_info':'Any other info?'}


class LogForm(forms.ModelForm):
    class Meta:
        model = Activity_Log
        fields = '__all__'

class ClusterForm(forms.ModelForm):
    class Meta:
        model = Cluster
        fields = ['user']


class SendMail(forms.ModelForm):
    email = forms.EmailField(label='Your email address')

    class Meta:
        model = ContactJACK_message
        fields = '__all__'
        exclude = ['datetime']
        labels = {'name': 'Your name',
                'phone_number': 'Your phone number',
                'message': 'How can we help?'}
