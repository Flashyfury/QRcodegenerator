from django import forms
from .models import QRCodeItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class QRCodeForm(forms.ModelForm):
    class Meta:
        model = QRCodeItem
        fields = ['data', 'fg_color', 'bg_color', 'size', 'logo']
        widgets = {
            'data': forms.TextInput(attrs={'placeholder': 'Enter text or URL', 'class': 'form-control'}),
            'fg_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control', 'value': '#000000'}),
            'bg_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control', 'value': '#ffffff'}),
            'size': forms.NumberInput(attrs={'class': 'form-control', 'min': 100, 'max': 2000}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
