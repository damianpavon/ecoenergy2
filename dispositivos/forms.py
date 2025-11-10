from django import forms
from .models import Device, Measurement, Category, Zone, Sensor, Alert

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'category', 'zone', 'reference']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'zone': forms.Select(attrs={'class': 'form-control'}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            try:
                organization = self.user.userprofile.organization
                self.fields['category'].queryset = Category.objects.filter(organization=organization)
                self.fields['zone'].queryset = Zone.objects.filter(organization=organization)
            except:
                self.fields['category'].queryset = Category.objects.none()
                self.fields['zone'].queryset = Zone.objects.none()

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['device', 'value', 'unit', 'date']
        widgets = {
            'device': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            try:
                organization = self.user.userprofile.organization
                self.fields['device'].queryset = Device.objects.filter(organization=organization)
            except:
                self.fields['device'].queryset = Device.objects.none()

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class SensorForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = ['device', 'name', 'type', 'unit']
        widgets = {
            'device': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            try:
                organization = self.user.userprofile.organization
                self.fields['device'].queryset = Device.objects.filter(organization=organization)
            except:
                self.fields['device'].queryset = Device.objects.none()

class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ['device', 'message', 'level']
        widgets = {
            'device': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            try:
                organization = self.user.userprofile.organization
                self.fields['device'].queryset = Device.objects.filter(organization=organization)
            except:
                self.fields['device'].queryset = Device.objects.none()
