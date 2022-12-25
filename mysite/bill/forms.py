from django import forms

class PersonForm(forms.Form):
    add_a_person = forms.CharField(required=True, max_length=500, min_length=3, strip=True)

class ItemForm(forms.Form):
    item_name = forms.CharField(required=True, max_length=500, min_length=3, strip=True)
    item_price = forms.DecimalField(max_digits=7, decimal_places=2)