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


    name = forms.CharField(label="Ім'я", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ім\'я'}))
    last_name = forms.CharField(label="Прізвище", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище'}))
    phone = forms.CharField(label="Телефон", widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'phonenumber', 'placeholder': "+38(000)-000-00-00"}))
    type_of_delivery = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'radio-input', 'id': 'typeOfDelivery'}), choices=CHOICES)
    city_ref_hidden = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'cityRefHidden'}))
    warehouse_id_hidden = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'warehouseRefHidden'}))
    courier = forms.CharField(required=False ,widget=forms.HiddenInput(attrs={'id': 'courierHidden'}))
    payment = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'radio-input2', 'id': 'payment'}), choices=CHOICES2)






