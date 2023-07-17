from django import forms
from blog.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input'}), label='Confirm Password')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'username', 'password', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-input'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-input'})
        self.fields['email'].widget.attrs.update({'class': 'form-input'})
        self.fields['username'].widget.attrs.update({'class': 'form-input'})

    def check_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            messages.error('Passwords do not match ')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email', 'username', 'profile_picture']
