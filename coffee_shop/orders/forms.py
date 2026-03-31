from django import forms


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=50, initial=1)


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    note = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}))
