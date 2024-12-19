from django import forms


class CheckoutUserDetails(forms.Form):
    name = forms.CharField(label="Ім'я", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Прізвище", widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label="Телефон", widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'phonenumber', 'placeholder': "+38(000)-000-00-00"}))

