from django import forms
from django.forms import Form

class SearchForm(Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Пошук товару'}))

class PriceFilterForm(Form):
    min_price = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'price-in',
                'id': 'minPriceInput'
            }
        )
    )
    max_price = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'price-in',
                'id': 'maxPriceInput'
            }
        )
    )

    def __init__(self, *args, **kwargs):

        min_product_price = kwargs.pop('min_price')
        max_product_price = kwargs.pop('max_price')
        super().__init__(*args, **kwargs)

        self.fields['min_price'].widget.attrs['min'] = min_product_price
        self.fields['min_price'].widget.attrs['max'] = max_product_price
        self.fields['max_price'].widget.attrs['min'] = min_product_price
        self.fields['max_price'].widget.attrs['max'] = max_product_price

        self.fields['min_price'].min_value = min_product_price
        self.fields['min_price'].max_value = max_product_price
        self.fields['max_price'].min_value = min_product_price
        self.fields['max_price'].max_value = max_product_price

    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')

        if int(max_price) < int(min_price):
            raise forms.ValidationError({'max_price': 'Максимальная цена не может быть меньше минимальной цены.'})

        return cleaned_data






