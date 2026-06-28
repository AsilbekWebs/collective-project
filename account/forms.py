from django import forms
from .models import Account



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'user_company', 'password']

    def clean_username(self):
        username = self.cleaned_data.get("username")

        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")

        return password




class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get("username")

        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")

        return password




class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'user_company', 'avatar']
