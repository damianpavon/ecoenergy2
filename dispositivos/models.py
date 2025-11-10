from django.db import models
from django.utils import timezone
from usuarios.models import Organization

# Constante de estados
STATUS = [
    ("ACTIVE", "Active"),
    ("INACTIVE", "Inactive"),
]

# QuerySet y Manager para soft delete
class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super().update(deleted_at=timezone.now())  # soft delete

    def hard_delete(self):
        return super().delete()


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)


# Clase base para herencia
class BaseModel(models.Model):
    status = models.CharField(max_length=10, choices=STATUS, default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True)   # fecha creación
    updated_at = models.DateTimeField(auto_now=True)       # última actualización
    deleted_at = models.DateTimeField(null=True, blank=True)  # borrado lógico

    objects = SoftDeleteManager()   # por defecto, solo activos
    all_objects = models.Manager()  # incluye eliminados

    class Meta:
        abstract = True
        ordering = ("-created_at",)

    def delete(self, using=None, keep_parents=False):
        """Soft delete (marca como eliminado)"""
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        """Elimina de la BD definitivamente"""
        super().delete()

    def restore(self):
        """Restaura un objeto borrado lógicamente"""
        self.deleted_at = None
        self.save()


# MODELOS DEL PROYECTO

class Category(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Zone(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Device(BaseModel):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="devices")
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="devices")
    reference = models.CharField(max_length=100, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Measurement(BaseModel):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="measurements")
    value = models.DecimalField(max_digits=12, decimal_places=3)
    unit = models.CharField(max_length=20, blank=True)
    date = models.DateTimeField(default=timezone.now)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.device.name} — {self.value} {self.unit}"


class Sensor(BaseModel):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="sensors")
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)  # Tipo de sensor, ej. temperatura, humedad
    unit = models.CharField(max_length=20)  # Unidad de medida, ej. °C, %
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.device.name} - {self.name}"


class Alert(BaseModel):
    LEVEL = [
        ("GRAVE", "Grave"),
        ("ALTA", "Alta"),
        ("MEDIA", "Media"),
    ]
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="alerts")
    message = models.CharField(max_length=250)
    level = models.CharField(max_length=10, choices=LEVEL, default="MEDIA")
    read = models.BooleanField(default=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"[{self.level}] {self.device.name} — {self.message}"
