from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from django.core.validators import FileExtensionValidator

# Constante de estados
ESTADOS = [
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
    status = models.CharField(max_length=10, choices=ESTADOS, default="ACTIVE")
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


class Organization(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    rut = models.CharField(max_length=12, unique=True, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

    def __str__(self):
        return f"{self.user.username} - {self.organization.name}"


class Module(models.Model):
    code = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    group = models.OneToOneField('auth.Group', on_delete=models.CASCADE, related_name="role")

    def __str__(self):
        return self.group.name


class RoleModulePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="module_perms")
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="role_perms")
    can_view = models.BooleanField(default=False)
    can_add = models.BooleanField(default=False)
    can_change = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    class Meta:
        unique_together = ("role", "module")

    def __str__(self):
        return f"{self.role} - {self.module} - View:{self.can_view} Add:{self.can_add} Change:{self.can_change} Delete:{self.can_delete}"
