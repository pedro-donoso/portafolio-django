from django import forms

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from .models import Producto, Categoria



class ProductoForm(forms.ModelForm):


    class Meta:
    model = Producto
    fields = ['nombre', 'descripcion', 'precio', 'stock', 'categoria', 'activo', 
        'imagen']
    widgets = {
    'nombre': forms.TextInput(attrs={
    'class': 'form-control',
    'placeholder': 'Ej: Laptop Dell Inspiron'
    }),
    'descripcion': forms.Textarea(attrs={
    'class': 'form-control',
    'rows': 4,
    'placeholder': 'Descripción detallada del producto...'
    }),
    'precio': forms.NumberInput(attrs={
    'class': 'form-control',
    'step': '0.01',
    'min': '0'
    }),
    'stock': forms.NumberInput(attrs={
    'class': 'form-control',
    'min': '0'
    }),
    'categoria': forms.Select(attrs={'class': 'form-control'}),
    'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    'imagen': forms.FileInput(attrs={'class': 'form-control'}),
    }

def clean_precio(self):
    precio = self.cleaned_data.get('precio')
    if precio and precio <= 0:
    raise forms.ValidationError("El precio debe ser mayor a cero")
    return precio

def clean_stock(self):
    stock = self.cleaned_data.get('stock')
    if stock < 0:
    raise forms.ValidationError("El stock no puede ser negativo")
    return stock


class CategoriaForm(forms.ModelForm):


    class Meta:
    model = Categoria
    fields = ['nombre', 'descripcion']
    widgets = {
    'nombre': forms.TextInput(attrs={
    'class': 'form-control',
    'placeholder': 'Ej: Electrónica'
    }),
    'descripcion': forms.Textarea(attrs={
    'class': 'form-control',
    'rows': 3,
    'placeholder': 'Descripción de la categoría...'
    }),
    }


class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(
    required=True,
    widget=forms.EmailInput(attrs={
    'class': 'form-control',
    'placeholder': 'correo@ejemplo.com'
    })
    )
    first_name = forms.CharField(
    max_length=100,
    required=True,
    label='Nombre',
    widget=forms.TextInput(attrs={
    'class': 'form-control',
    'placeholder': 'Tu nombre'
    })
    )
    last_name = forms.CharField(
    max_length=100,
    required=True,
    label='Apellido',
    widget=forms.TextInput(attrs={
    'class': 'form-control',
    'placeholder': 'Tu apellido'
    })
    )


class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    widgets = {
    'username': forms.TextInput(attrs={
    'class': 'form-control',
    'placeholder': 'Nombre de usuario'
    }),
    }

def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['password1'].widget.attrs.update({
    'class': 'form-control',
    'placeholder': 'Contraseña'
    })
    self.fields['password2'].widget.attrs.update({
    'class': 'form-control',
    'placeholder': 'Confirmar contraseña'
    })

def save(self, commit=True):
    user = super().save(commit=False)
    user.email = self.cleaned_data['email']
    user.first_name = self.cleaned_data['first_name']
    user.last_name = self.cleaned_data['last_name']
    if commit:
    user.save()
    return user
