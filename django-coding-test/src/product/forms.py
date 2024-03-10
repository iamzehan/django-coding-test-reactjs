from django.forms import forms, ModelForm, CharField, TextInput, Textarea, BooleanField, CheckboxInput

from product.models import Variant


class VariantForm(ModelForm):
    class Meta:
        model = Variant
        fields = '__all__'
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'active': CheckboxInput(attrs={'class': 'form-check-input', 'id': 'active'})
        }

class ProductFilterForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Product Title', 'class': 'form-control'}), required=False)
    variant = forms.CharField(label='', widget=forms.Select(choices=[('', '--Select A Variant--')], attrs={'class': 'form-control'}), required=False)
    price_from = forms.FloatField(label='', widget=forms.TextInput(attrs={'placeholder': 'From', 'class': 'form-control'}), required=False)
    price_to = forms.FloatField(label='', widget=forms.TextInput(attrs={'placeholder': 'To', 'class': 'form-control'}), required=False)
    date = forms.DateField(label='', widget=forms.DateInput(attrs={'placeholder': 'Date', 'class': 'form-control'}), required=False)