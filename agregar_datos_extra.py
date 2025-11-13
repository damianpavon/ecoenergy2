from django.contrib.auth.models import User
from dispositivos.models import Zone, Device, Category, Alert, Measurement, Organization
from django.utils import timezone
from random import choice, randint, uniform

# ====== ORGANIZACIÓN ======
org, _ = Organization.objects.get_or_create(name="EcoEnergy Corp")

# ====== USUARIO BASE ======
user, _ = User.objects.get_or_create(username="arayac961", email="arayac961@gmail.com")

# ====== CATEGORÍAS ADICIONALES ======
categorias_extra = [
    ("CO2", "Sensores de dióxido de carbono"),
    ("Luz", "Medidores de iluminación ambiental"),
    ("Movimiento", "Sensores de movimiento"),
    ("Flujo", "Medidores de flujo de agua o aire"),
    ("Voltaje", "Sensores de voltaje eléctrico"),
    ("Corriente", "Sensores de corriente eléctrica"),
    ("Presencia", "Sensores de presencia humana"),
]

categorias_creadas = []
for nombre, descripcion in categorias_extra:
    cat, _ = Category.objects.get_or_create(
        name=nombre,
        description=descripcion,
        organization=org
    )
    categorias_creadas.append(cat)

print(f"✅ {len(categorias_creadas)} nuevas categorías agregadas.")

# ====== DISPOSITIVOS ADICIONALES ======
zonas = list(Zone.objects.all())
categorias = list(Category.objects.filter(organization=org))
dispositivos_creados = []

for i in range(1, 21):
    d, _ = Device.objects.get_or_create(
        name=f"Dispositivo Extra {i}",
        category=choice(categorias),
        zone=choice(zonas),
        organization=org,
        status="Activo"
    )
    dispositivos_creados.append(d)

print(f"✅ {len(dispositivos_creados)} dispositivos nuevos agregados.")

# ====== ALERTAS ADICIONALES ======
niveles = ["GRAVE", "ALTA", "MEDIA"]
for _ in range(20):
    Alert.objects.create(
        device=choice(dispositivos_creados),
        message="Nueva alerta generada automáticamente",
        level=choice(niveles),
        created_at=timezone.now() - timezone.timedelta(days=randint(0, 6))
    )

print("✅ 20 alertas nuevas creadas.")

# ====== MEDICIONES ADICIONALES ======
for _ in range(40):
    Measurement.objects.create(
        device=choice(dispositivos_creados),
        value=round(uniform(10.0, 99.9), 2),
        date=timezone.now() - timezone.timedelta(hours=randint(1, 72))
    )

print("✅ 40 mediciones nuevas registradas.")

print("🎉 Datos adicionales cargados exitosamente en la base de datos.")
