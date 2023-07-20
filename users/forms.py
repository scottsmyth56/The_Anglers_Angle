from django import forms
from blog.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input form-control'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input form-control'}),
        label='Confirm Password')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'username', 'password', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-input form-control'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-input form-control'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-input form-control'})
        self.fields['username'].widget.attrs.update(
            {'class': 'form-input form-control'})

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username:
            self.add_error('username', 'Username is required')

        if not password:
            self.add_error('password', 'Password is required')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise ValidationError("Invalid username or password")

        return cleaned_data


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email', 'username', 'profile_picture']


class ResetPasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input form-control'}),
        label='Current Password')
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input form-control'}),
        label='New Password')
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input form-control'}),
        label='Confirm New Password')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_current_password(self):
        """
        Validates that the current_password field contains the correct password for the current user.
        """
        current_password = self.cleaned_data.get('current_password')

        if not check_password(current_password, self.user.password):
            raise forms.ValidationError(
                'Your current password was entered incorrectly. Please enter it again.')

        return current_password

    def clean_confirm_new_password(self):
        """
        Validates that the new_password and confirm_new_password fields match.
        """
        new_password = self.cleaned_data.get('new_password')
        confirm_new_password = self.cleaned_data.get('confirm_new_password')

        if new_password and confirm_new_password:
            if new_password != confirm_new_password:
                raise forms.ValidationError(
                    'Your new passwords do not match. Please try again.')

        return confirm_new_password

    def save(self, commit=True):
        """
        Sets the user's password to the value provided in the confirm_new_password field.
        """
        self.user.set_password(self.cleaned_data['confirm_new_password'])
        if commit:
            self.user.save()
