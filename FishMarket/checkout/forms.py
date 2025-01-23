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
    type_of_delivery = forms.ChoiceField(required=False, widget=forms.RadioSelect(
        attrs={'class': 'radio-input', 'id': 'typeOfDelivery'}), choices=CHOICES)
    city_ref_hidden = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'cityRefHidden'}))
    courier = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'courierHidden'}))
    payment = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'radio-input2', 'id': 'payment'}),
                                choices=CHOICES2)
    user_id = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'user_authenticated'}))
    delivery_address = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'full_address'}))
    warehouse_number = forms.CharField(required=False,
                                              widget=forms.HiddenInput(attrs={'id': 'warehouseRefHidden'}))

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        print(len(phone))

        if not len(phone) == 18:
            raise forms.ValidationError('Номер телефону має бути повний')

        return phone

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.isalpha():
            raise forms.ValidationError('Ім\'я не повинно містити символи чи цифри.')

        return name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError('Прізвище не повинно містити символи чи цифри.')

        return last_name

    def clean(self):
        cleaned_data = super().clean()
        courier = cleaned_data.get('courier')
        warehouse_id_hidden = cleaned_data.get('warehouse_id_hidden')
        city_ref_hidden = cleaned_data.get('city_ref_hidden')

        if courier and warehouse_id_hidden and city_ref_hidden:
            raise forms.ValidationError('Помилка вибору доставки. Переконайтеся, що ви вибрали один вид доставки.')

        if not courier and not warehouse_id_hidden and not city_ref_hidden:
            raise forms.ValidationError('Помилка вибору доставки. Переконайтеся, що ви вибрали вид доставки.')

        return cleaned_data
