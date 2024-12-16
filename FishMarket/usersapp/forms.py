from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, \
    SetPasswordForm
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django import forms

from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Поштова адреса'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Підтвердження пароля'

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введіть вашу пошту @',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введіть пароль',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введіть пароль повторно',
        })

    def clean_email(self):
        email = self.cleaned_data['email']
        email = email.lower()
        return email


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.fields['username'].label = ''
        self.fields['password'].label = ''

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введіть вашу пошту @',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введіть пароль',
        })

    def clean_username(self):
        username = self.cleaned_data['username']

        if '@' not in username:
            raise ValidationError('Потрібно вказати повну поштову адресу ___@__.__')
        elif '.' not in username:
            raise ValidationError('Потрібно вказати повну поштову адресу ___@__.__')
        return username


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старий Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Старий Пароль'}))
    new_password1 = forms.CharField(label='Новий пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Новий пароль'}))
    new_password2 = forms.CharField(label='Новий пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Новий пароль 2'}))

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].label = ''
        self.fields['new_password1'].label = ''
        self.fields['new_password2'].label = ''

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = ''
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введіть вашу пошту @',
        })

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].label = ''
        self.fields['new_password2'].label = ''

        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Пароль 1',
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Повторно Пароль',
        })

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'last_name', 'email', 'phone_number')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ім'я"}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище:'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Електронна пошта:'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'id': 'phonenumber', 'placeholder': "+38(000)-000-00-00"}),
        }


