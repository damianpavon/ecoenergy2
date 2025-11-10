from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .models import UserProfile, Organization
from django.core.exceptions import ValidationError
import re

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label="First Name")
    last_name = forms.CharField(max_length=30, required=False, label="Last Name")
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = UserProfile
        fields = ['rut', 'telefono', 'direccion', 'profile_image']
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if rut:
            # Basic RUT validation (Chilean format)
            if not re.match(r'^\d{1,8}-[0-9kK]$', rut):
                raise ValidationError("Invalid RUT format. Use XXXXXXXX-X")
        return rut

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            # Basic phone validation
            if not re.match(r'^\+?[\d\s\-\(\)]+$', telefono):
                raise ValidationError("Invalid phone number format")
        return telefono

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        if image:
            # Check file size (max 5MB)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Image file too large ( > 5MB )")
            # Check dimensions
            from PIL import Image as PILImage
            img = PILImage.open(image)
            if img.width > 1000 or img.height > 1000:
                raise ValidationError("Image dimensions too large (max 1000x1000)")
        return image

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one number")
        return password
