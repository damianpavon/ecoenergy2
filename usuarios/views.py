from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import UserProfile
from dispositivos.models import Organization
from .forms import UserProfileForm, CustomPasswordChangeForm

class SimpleLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

class SimpleRegisterForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    organization_name = forms.CharField(label="Organization Name")
    organization_email = forms.EmailField(label="Organization Email")

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_organization_email(self):
        org_email = self.cleaned_data['organization_email']
        if Organization.objects.filter(email=org_email).exists():
            raise forms.ValidationError("An organization with this email already exists.")
        return org_email

def login_view(request):
    if request.method == "POST":
        form = SimpleLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on user role
                if user.groups.filter(name='Admin').exists():
                    return redirect('admin_dashboard')
                elif user.groups.filter(name='Manager').exists():
                    return redirect('dashboard')
                else:
                    return redirect('dashboard')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Please correct the errors.")
    else:
        form = SimpleLoginForm()
    return render(request, "usuarios/login.html", {"form": form})

def register_view(request):
    if request.method == "POST":
        form = SimpleRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            org_name = form.cleaned_data['organization_name']
            org_email = form.cleaned_data['organization_email']
            user = User.objects.create_user(username=email, email=email, password=password)
            org = Organization.objects.create(name=org_name, email=org_email)
            UserProfile.objects.create(user=user, organization=org)
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please correct the errors.")
    else:
        form = SimpleRegisterForm()
    return render(request, "usuarios/register.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('login')

def password_reset_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            # Simulate sending email
            messages.success(request, "Instructions to reset your password have been sent to your email.")
            return redirect('login')
        else:
            messages.error(request, "Please enter a valid email address.")
    else:
        form = PasswordResetForm()
    return render(request, "usuarios/password_reset.html", {"form": form})

class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label="First Name")
    last_name = forms.CharField(max_length=30, required=False, label="Last Name")
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = UserProfile
        fields = ['telefono', 'direccion', 'profile_image']
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3}),
            'profile_image': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image file too large ( > 5MB )")
        return image

@login_required
def edit_profile_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=user_profile, user=request.user)
        if form.is_valid():
            # Update User model
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()

            # Update UserProfile
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('edit_profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EditProfileForm(instance=user_profile, user=request.user)

    return render(request, "usuarios/edit_profile.html", {"form": form})

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Current Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Current password is incorrect.")
        return old_password

    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least one number.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("New passwords do not match.")
        return cleaned_data

@login_required
def change_password_view(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['new_password1'])
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Password changed successfully.")
            return redirect('change_password')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ChangePasswordForm(request.user)

    return render(request, "usuarios/change_password.html", {"form": form})
