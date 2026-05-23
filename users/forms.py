from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Speciality


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
            field.widget.attrs.update({'class': 'input input--text'}) 

class ProfileForm(forms.ModelForm):
    """
    Form for editing user profile information, including both User and Profile model fields.
    """
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username', 'county', 'bio', 'profile_image', 
                  'whatsapp_link', 'website', 'social_twitter', 'youtube']
        #fields = '__all__' # <--- Alternative to explicitly listing fields, but less secure if new fields are added to the model in the future without updating the form. Use with caution.


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Programmatic Styling Loop: 
        # Inject modern form classes to every field widget
        for name, field in self.fields.items():
            #field.widget.attrs.update({'class': 'input input--text'})
            field.widget.attrs.update({'class': 'input input--text'})         


class SpecialityForm(forms.ModelForm):
    """
    Form for creating and editing Speciality instances, which represent 
    specific areas of expertise or focus for farmers.
    """
    class Meta:
        model = Speciality
        #fields = ['name', 'description']
        fields = '__all__' # <--- Alternative to explicitly listing fields, but less secure if new fields are added to the model in the future without updating the form. Use with caution.
        exclude = ['owner'] # Exclude the owner field since it will be set programmatically in the view based on the logged-in user.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Programmatic Styling Loop: 
        # Inject modern form classes to every field widget
        for name, field in self.fields.items():
            #field.widget.attrs.update({'class': 'input input--text'})
            field.widget.attrs.update({'class': 'input'})            