from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', )

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
