from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1']
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        del self.fields['password2']
    def clean(self):
        super(UserRegisterForm, self).clean()
        name = self.cleaned_data.get('username')
        if str(name).lower()=='admin':
            self._errors['username'] = self.error_class(['Username can not be Admin.'])
        return self.cleaned_data

class add_pass_form(forms.Form):
    name = forms.CharField(label="name", max_length=100, required=True)
    username = forms.CharField(label="username", max_length=100, required=True)
    password = forms.CharField(label="password", max_length=50, required=True) 
    
        
class edit_pass_form(forms.Form):
    name = forms.CharField(label="name", max_length=100, required=True)
    username = forms.CharField(label="username", max_length=100, required=True)
    password = forms.CharField(label="password", max_length=50, required=True) 

class delete_pass_form(forms.Form):
    names = forms.CharField(label="names")
    def clean(self):
        super(delete_pass_form, self).clean()
        names = self.cleaned_data.get('names')
        if len(str(names).strip().replace('[','').replace(']',''))<=2:
            self._errors['names'] = self.error_class(['Please select at least one record to be deleted.'])
        return self.cleaned_data