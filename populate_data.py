import os
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoreo.settings')
django.setup()

from usuarios.models import Organization, UserProfile
from dispositivos.models import Category, Zone, Device, Sensor, Measurement, Alert
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Crear organización
org, created = Organization.objects.get_or_create(name='EcoEnergy Corp', defaults={'email': 'info@ecoenergy.com'})

# Crear categorías
categories = [
    {'name': 'Temperatura', 'description': 'Sensores de temperatura'},
    {'name': 'Humedad', 'description': 'Sensores de humedad'},
    {'name': 'Presión', 'description': 'Sensores de presión'},
    {'name': 'Energía', 'description': 'Medidores de energía'},
    {'name': 'Vibración', 'description': 'Sensores de vibración'},
    {'name': 'Ruido', 'description': 'Sensores de ruido ambiental'},
]

for cat_data in categories:
    Category.objects.get_or_create(name=cat_data['name'], defaults={'description': cat_data['description'], 'organization': org})

# Crear zonas
zones = [
    {'name': 'Zona Norte', 'description': 'Área norte de la instalación'},
    {'name': 'Zona Sur', 'description': 'Área sur de la instalación'},
    {'name': 'Zona Este', 'description': 'Área este de la instalación'},
    {'name': 'Zona Oeste', 'description': 'Área oeste de la instalación'},
    {'name': 'Zona Central', 'description': 'Área central de la instalación'},
]

for zone_data in zones:
    Zone.objects.get_or_create(name=zone_data['name'], defaults={'description': zone_data['description'], 'organization': org})

# Crear dispositivos
devices = [
    {'name': 'Dispositivo 1', 'category': Category.objects.get(name='Temperatura'), 'zone': Zone.objects.get(name='Zona Norte'), 'reference': 'REF001'},
    {'name': 'Dispositivo 2', 'category': Category.objects.get(name='Humedad'), 'zone': Zone.objects.get(name='Zona Sur'), 'reference': 'REF002'},
    {'name': 'Dispositivo 3', 'category': Category.objects.get(name='Presión'), 'zone': Zone.objects.get(name='Zona Este'), 'reference': 'REF003'},
    {'name': 'Dispositivo 4', 'category': Category.objects.get(name='Energía'), 'zone': Zone.objects.get(name='Zona Oeste'), 'reference': 'REF004'},
    {'name': 'Dispositivo 5', 'category': Category.objects.get(name='Vibración'), 'zone': Zone.objects.get(name='Zona Central'), 'reference': 'REF005'},
    {'name': 'Dispositivo 6', 'category': Category.objects.get(name='Ruido'), 'zone': Zone.objects.get(name='Zona Central'), 'reference': 'REF006'},
]

for dev_data in devices:
    Device.objects.get_or_create(name=dev_data['name'], defaults={'category': dev_data['category'], 'zone': dev_data['zone'], 'reference': dev_data['reference'], 'organization': org})

# Crear sensores
sensors = [
    {'device': Device.objects.get(name='Dispositivo 1'), 'name': 'Sensor Temp 1', 'type': 'Temperatura', 'unit': '°C'},
    {'device': Device.objects.get(name='Dispositivo 1'), 'name': 'Sensor Temp 2', 'type': 'Temperatura', 'unit': '°C'},
    {'device': Device.objects.get(name='Dispositivo 2'), 'name': 'Sensor Hum 1', 'type': 'Humedad', 'unit': '%'},
    {'device': Device.objects.get(name='Dispositivo 2'), 'name': 'Sensor Hum 2', 'type': 'Humedad', 'unit': '%'},
    {'device': Device.objects.get(name='Dispositivo 3'), 'name': 'Sensor Pres 1', 'type': 'Presión', 'unit': 'Pa'},
    {'device': Device.objects.get(name='Dispositivo 4'), 'name': 'Sensor Ener 1', 'type': 'Energía', 'unit': 'kWh'},
    {'device': Device.objects.get(name='Dispositivo 5'), 'name': 'Sensor Vib 1', 'type': 'Vibración', 'unit': 'Hz'},
    {'device': Device.objects.get(name='Dispositivo 6'), 'name': 'Sensor Ruido 1', 'type': 'Ruido', 'unit': 'dB'},
]

for sen_data in sensors:
    Sensor.objects.get_or_create(device=sen_data['device'], name=sen_data['name'], defaults={'type': sen_data['type'], 'unit': sen_data['unit'], 'organization': org})

# Crear mediciones
now = timezone.now()
measurements = [
    {'device': Device.objects.get(name='Dispositivo 1'), 'value': 25.5, 'unit': '°C', 'date': now - timedelta(hours=1)},
    {'device': Device.objects.get(name='Dispositivo 2'), 'value': 60.0, 'unit': '%', 'date': now - timedelta(hours=2)},
    {'device': Device.objects.get(name='Dispositivo 3'), 'value': 101325.0, 'unit': 'Pa', 'date': now - timedelta(hours=3)},
    {'device': Device.objects.get(name='Dispositivo 4'), 'value': 150.0, 'unit': 'kWh', 'date': now - timedelta(hours=4)},
    {'device': Device.objects.get(name='Dispositivo 5'), 'value': 50.0, 'unit': 'Hz', 'date': now - timedelta(hours=5)},
    {'device': Device.objects.get(name='Dispositivo 6'), 'value': 70.0, 'unit': 'dB', 'date': now - timedelta(hours=6)},
]

for meas_data in measurements:
    Measurement.objects.create(device=meas_data['device'], value=meas_data['value'], unit=meas_data['unit'], date=meas_data['date'], organization=org)

# Crear alertas
alerts = [
    {'device': Device.objects.get(name='Dispositivo 1'), 'message': 'Temperatura alta detectada', 'level': 'ALTA', 'created_at': now - timedelta(days=1)},
    {'device': Device.objects.get(name='Dispositivo 2'), 'message': 'Humedad baja', 'level': 'MEDIA', 'created_at': now - timedelta(days=2)},
    {'device': Device.objects.get(name='Dispositivo 3'), 'message': 'Presión inestable', 'level': 'GRAVE', 'created_at': now - timedelta(days=3)},
    {'device': Device.objects.get(name='Dispositivo 4'), 'message': 'Consumo de energía elevado', 'level': 'ALTA', 'created_at': now - timedelta(days=4)},
    {'device': Device.objects.get(name='Dispositivo 5'), 'message': 'Vibración anormal detectada', 'level': 'MEDIA', 'created_at': now - timedelta(days=1)},
    {'device': Device.objects.get(name='Dispositivo 6'), 'message': 'Ruido excesivo', 'level': 'ALTA', 'created_at': now - timedelta(days=2)},
]

for alert_data in alerts:
    Alert.objects.create(device=alert_data['device'], message=alert_data['message'], level=alert_data['level'], created_at=alert_data['created_at'], organization=org)

# Crear superusuario
user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@ecoenergy.com', 'is_superuser': True, 'is_staff': True})
if created:
    user.set_password('admin123')
    user.save()

# Crear perfil de usuario
UserProfile.objects.get_or_create(user=user, organization=org)

print("Datos de ejemplo y superusuario agregados exitosamente.")
print("Usuario: admin")
print("Contraseña: admin123")
