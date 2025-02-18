from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'location', 'date_of_birth']

        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
        }

