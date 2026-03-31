from django import forms


class ProductSearchForm(forms.Form):
    """Form tìm kiếm sản phẩm cơ bản."""

    query = forms.CharField(
        label='Từ khóa',
        max_length=120,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Tìm cà phê...'}),
    )
