from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        min_length=6,
        help_text='Username must be at least 6 characters long.',
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9]*$',
                message='Username can only contain letters and numbers.',
            ),
        ]
    )
    
    email = forms.EmailField(required=True)
    
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        help_text='''
        Password must contain:
        • At least 6 characters
        • At least one uppercase letter
        • At least one lowercase letter
        • At least one number
        • At least one special character
        '''
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
        
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 6:
            raise ValidationError('Password must be at least 6 characters long.')
        if not any(char.isupper() for char in password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not any(char.islower() for char in password):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain at least one number.')
        if not any(not char.isalnum() for char in password):
            raise ValidationError('Password must contain at least one special character.')
        return password

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))