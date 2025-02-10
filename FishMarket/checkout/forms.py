from django import forms
from django.core.exceptions import ValidationError


class CheckoutUserForm(forms.Form):
    CHOICES = [
        ('1', 'Відділення'),
        ('2', 'Поштомат'),
        ('3', "Кур'єр")
    ]

    CHOICES2 = [
        ('1', 'Готівка при отриманні'),
        ('2', 'Оплата на картку')
    ]

    name = forms.CharField(label="Ім'я",
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ім\'я'}))
    last_name = forms.CharField(label="Прізвище",
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище'}))
    phone = forms.CharField(label="Телефон", widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'phonenumber', 'placeholder': "+38(000)-000-00-00"}))
    delivery_type = forms.ChoiceField(required=False, widget=forms.RadioSelect(
        attrs={'class': 'radio-input', 'id': 'typeOfDelivery'}), choices=CHOICES)
    payment_type = forms.ChoiceField(required=True, widget=forms.RadioSelect(
        attrs={'class': 'radio-payment-choose', 'id': 'paymentType'}), choices=CHOICES2)
    user_address = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'user_address'}))
    address_from_memory = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(
        attrs={'id': 'userAddressFromMemory', 'style': 'display: none;'}))

    def clean(self):
        cleaned_data = super().clean()

        user_address = cleaned_data.get('user_address')
        delivery_type = cleaned_data.get('delivery_type')
        warehouse_number = cleaned_data.get('warehouse_number')
        address_from_memory = cleaned_data.get('address_from_memory')

        if address_from_memory and delivery_type:
            raise ValidationError('Необхідно вибрати лише одну адресу доставки')

        if not user_address:
            raise ValidationError('Виберіть тип доставки')

        return cleaned_data
