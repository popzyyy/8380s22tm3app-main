from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Unit, Product, Category, Order, OrderItem, User


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ('name', 'description')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'price', 'available', 'product_unit', 'product_category')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address', 'postal_code', 'city')


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('order', 'product', 'price', 'quantity', 'created_date')


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class CurrencyForm(forms.Form):

    currency_code = ("AED",
              "AFN",
              "ALL",
              "AMD",
              "ANG",
              "AOA",
              "ARS",
              "AUD",
              "AWG",
              "AZN",
              "BAM",
              "BBD",
              "BDT",
              "BGN",
              "BHD",
              "BIF",
              "BMD",
              "BND",
              "BOB",
              "BRL",
              "BSD",
              "BTC",
              "BTN",
              "BWP",
              "BYR",
              "BZD",
              "CAD",
              "CDF",
              "CHF",
              "CLF",
              "CLP",
              "CNY",
              "COP",
              "CRC",
              "CUC",
              "CUP",
              "CVE",
              "CZK",
              "DJF",
              "DKK",
              "DOP",
              "DZD",
              "EGP",
              "ERN",
              "ETB",
              "EUR",
              "FJD",
              "FKP",
              "GBP",
              "GEL",
              "GGP",
              "GHS",
              "GIP",
              "GMD",
              "GNF",
              "GTQ",
              "GYD",
              "HKD",
              "HNL",
              "HRK",
              "HTG",
              "HUF",
              "IDR",
              "ILS",
              "IMP",
              "INR",
              "IQD",
              "IRR",
              "ISK",
              "JEP",
              "JMD",
              "JOD",
              "JPY",
              "KES",
              "KGS",
              "KHR",
              "KMF",
              "KPW",
              "KRW",
              "KWD",
              "KYD",
              "KZT",
              "LAK",
              "LBP",
              "LKR",
              "LRD",
              "LSL",
              "LTL",
              "LVL",
              "LYD",
              "MAD",
              "MDL",
              "MGA",
              "MKD",
              "MMK",
              "MNT",
              "MOP",
              "MRO",
              "MUR",
              "MVR",
              "MWK",
              "MXN",
              "MYR",
              "MZN",
              "NAD",
              "NGN",
              "NIO",
              "NOK",
              "NPR",
              "NZD",
              "OMR",
              "PAB",
              "PEN",
              "PGK",
              "PHP",
              "PKR",
              "PLN",
              "PYG",
              "QAR",
              "RON",
              "RSD",
              "RUB",
              "RWF",
              "SAR",
              "SBD",
              "SCR",
              "SDG",
              "SEK",
              "SGD",
              "SHP",
              "SLL",
              "SOS",
              "SRD",
              "STD",
              "SVC",
              "SYP",
              "SZL",
              "THB",
              "TJS",
              "TMT",
              "TND",
              "TOP",
              "TRY",
              "TTD",
              "TWD",
              "TZS",
              "UAH",
              "UGX",
              "USD",
              "UYU",
              "UZS",
              "VEF",
              "VND",
              "VUV",
              "WST",
              "XAF",
              "XAG",
              "XAU",
              "XCD",
              "XDR",
              "XOF",
              "XPF",
              "YER",
              "ZAR",
              "ZMK",
              "ZMW",
              "ZWL")
    #currency = forms.ChoiceField(choices=currency_code, label='currency')
    currencies = forms.CharField(label='Select Desired Currency', widget=forms.Select(choices=currency_code))