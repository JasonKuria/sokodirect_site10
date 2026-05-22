from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    """
    Extends the native Django UserCreationForm to explicitly capture 
    essential farmer profile details during account initialization.
    """
    class Meta:
        model = User # Use the built-in User model for authentication and basic user data
        # Re-arrange ordering: capture structural baseline contact data first
        # fields = ['first_name', 'email', 'username', 'password1', 'password2']
        fields = ['first_name', 'email', 'username']        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Override structural form labels for cleaner presentation fields
        self.fields['first_name'].label = "Full Name"
        self.fields['first_name'].required = True
        self.fields['email'].required = True