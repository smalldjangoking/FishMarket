from django import forms


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
    user_saved_address_id = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'user_saved_address_id'}))
    courier = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'courierHidden'}))

