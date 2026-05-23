from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    """
    Extends the native Django UserCreationForm to explicitly capture 
    essential farmer profile details during account initialization.
    """
    """
    Subclasses Django's UserCreationForm to explicitly append CSS styling hooks 
    and custom display attributes to all field elements during creation.
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

        # Programmatic Styling Loop: 
        # Inject modern form classes to every field widget
        for name, field in self.fields.items():
            #field.widget.attrs.update({'class': 'input input--text'})
            field.widget.attrs.update({'class': 'input'})            