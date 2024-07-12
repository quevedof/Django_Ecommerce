from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# form to allow users to sign up
class CreateUserForm(UserCreationForm):
    # initilize fields along with their corresponding widgets
    username=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username', 'id':'username'}))
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name', 'id':'firstName'}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name', 'id':'lastName'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email', 'id':'email'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'id':'password'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat password', 'id':'confirmPassword'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1' ,'password2']
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
    