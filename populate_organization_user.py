import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoreo.settings')
django.setup()

from django.contrib.auth.models import User
from usuarios.models import UserProfile, Organization
from dispositivos.models import Category, Zone, Device, Measurement, Alert
from django.utils import timezone
from datetime import timedelta

def assign_organization_to_user():
    # Obtener usuario
    try:
        user = User.objects.get(email='carlos.araya121@inacapmail.cl')
    except User.DoesNotExist:
        print("Usuario no encontrado")
        return

    # Obtener o crear organización
    organization, created = Organization.objects.get_or_create(name='Organización Demo')

    # Asignar organización al perfil de usuario
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.organization = organization
    profile.save()
    print(f"Organización asignada a usuario {user.email}")

    # Poblar datos de ejemplo si no existen
    if not Category.objects.filter(organization=organization).exists():
        cat1 = Category.objects.create(name='Categoría 1', description='Descripción 1', organization=organization)
        cat2 = Category.objects.create(name='Categoría 2', description='Descripción 2', organization=organization)
        print("Categorías creadas")

    if not Zone.objects.filter(organization=organization).exists():
        zone1 = Zone.objects.create(name='Zona 1', organization=organization)
        zone2 = Zone.objects.create(name='Zona 2', organization=organization)
        print("Zonas creadas")

    if not Device.objects.filter(organization=organization).exists():
        device1 = Device.objects.create(name='Dispositivo 1', category=cat1, zone=zone1, organization=organization)
        device2 = Device.objects.create(name='Dispositivo 2', category=cat2, zone=zone2, organization=organization)
        print("Dispositivos creados")

    if not Measurement.objects.filter(device__organization=organization).exists():
        Measurement.objects.create(device=device1, date=timezone.now(), value=23.5, unit='°C')
        Measurement.objects.create(device=device2, date=timezone.now() - timedelta(days=1), value=45.0, unit='%')
        print("Mediciones creadas")

    if not Alert.objects.filter(device__organization=organization).exists():
        Alert.objects.create(device=device1, level='ALTA', message='Alerta alta ejemplo', created_at=timezone.now())
        Alert.objects.create(device=device2, level='MEDIA', message='Alerta media ejemplo', created_at=timezone.now())
        print("Alertas creadas")

def create_test_users():
    from django.contrib.auth.models import Group

    # Obtener organización
    organization, created = Organization.objects.get_or_create(name='Organización Demo')

    # Crear usuarios de prueba
    users_data = [
        {'username': 'admin_user', 'email': 'admin@example.com', 'password': 'admin123', 'group': 'Admin', 'rut': '12345678-9'},
        {'username': 'manager_user', 'email': 'manager@example.com', 'password': 'manager123', 'group': 'Manager', 'rut': '87654321-0'},
        {'username': 'user_user', 'email': 'user@example.com', 'password': 'user123', 'group': 'User', 'rut': '11223344-5'},
    ]

    for data in users_data:
        user, created = User.objects.get_or_create(username=data['username'], defaults={
            'email': data['email'],
            'is_staff': True,
            'is_superuser': False
        })
        if created:
            user.set_password(data['password'])
            user.save()
            print(f"Usuario {user.username} creado")

        # Asignar grupo
        group = Group.objects.get(name=data['group'])
        user.groups.add(group)

        # Crear perfil
        profile, created = UserProfile.objects.get_or_create(user=user, defaults={
            'organization': organization,
            'rut': data['rut']
        })
        if not created:
            profile.organization = organization
            profile.rut = data['rut']
            profile.save()
        print(f"Perfil asignado a {user.username}")

if __name__ == '__main__':
    import django
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoreo.settings')
    django.setup()
    assign_organization_to_user()
    create_test_users()
