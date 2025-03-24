from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import NguoiDung

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    DiaChi = forms.CharField(max_length=100, required=False)
    SoDienThoai = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'DiaChi', 'SoDienThoai']
