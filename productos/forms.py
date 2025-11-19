from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'activo', 'imagen_url']
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
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'imagen_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://ejemplo.com/imagen.jpg'
            }),
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

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        })
    )
    first_name = forms.CharField(
        max_length=100,
        required=True,
        label="Nombre",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        label="Apellido",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu apellido'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nombre de Usuario',
        }
        help_texts = {
            'username': '150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'nombre_usuario'
            }),
        }
        error_messages = {
            'username': {
                'required': 'Este campo es obligatorio.',
                'unique': 'Ya existe un usuario con este nombre.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personalizar campo username
        self.fields['username'].error_messages = {
            'required': 'Este campo es obligatorio.',
            'unique': 'Ya existe un usuario con este nombre.',
            'invalid': 'Ingresa un nombre de usuario válido.',
        }

        # Personalizar campo password1
        self.fields['password1'].label = 'Contraseña'
        self.fields['password1'].help_text = mark_safe('''
        <ul class="small text-muted mb-0">
            <li>Tu contraseña no puede ser muy similar a tu otra información personal.</li>
            <li>Tu contraseña debe contener al menos 8 caracteres.</li>
            <li>Tu contraseña no puede ser una contraseña comúnmente usada.</li>
            <li>Tu contraseña no puede ser completamente numérica.</li>
        </ul>
        ''')
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña'
        })
        self.fields['password1'].error_messages = {
            'required': 'Este campo es obligatorio.',
        }

        # Personalizar campo password2
        self.fields['password2'].label = 'Confirmar Contraseña'
        self.fields['password2'].help_text = 'Ingresa la misma contraseña que antes, para verificación.'
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirma tu contraseña'
        })
        self.fields['password2'].error_messages = {
            'required': 'Este campo es obligatorio.',
        }

        # Personalizar campo email
        self.fields['email'].error_messages = {
            'required': 'Este campo es obligatorio.',
            'invalid': 'Ingresa un correo electrónico válido.',
        }

        # Personalizar campos nombre y apellido
        self.fields['first_name'].error_messages = {
            'required': 'Este campo es obligatorio.',
        }
        self.fields['last_name'].error_messages = {
            'required': 'Este campo es obligatorio.',
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError('Las contraseñas no coinciden.')

        return password2

    def _post_clean(self):
        super()._post_clean()
        # Traducir mensajes de validación de contraseña
        password = self.cleaned_data.get('password2')
        if password:
            try:
                from django.contrib.auth.password_validation import validate_password
                validate_password(password, self.instance)
            except ValidationError as error:
                # Traducir mensajes de error
                translated_messages = []
                for message in error.messages:
                    if 'too similar' in message.lower():
                        translated_messages.append('La contraseña es muy similar a tu información personal.')
                    elif 'at least' in message.lower() or 'too short' in message.lower():
                        translated_messages.append('La contraseña debe contener al menos 8 caracteres.')
                    elif 'common' in message.lower():
                        translated_messages.append('Esta contraseña es muy común.')
                    elif 'numeric' in message.lower() or 'entirely' in message.lower():
                        translated_messages.append('La contraseña no puede ser completamente numérica.')
                    else:
                        translated_messages.append(message)

                self.add_error('password2', ValidationError(translated_messages))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
