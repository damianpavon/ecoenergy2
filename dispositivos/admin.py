from django.contrib import admin
from .models import Category, Zone, Device, Measurement, Sensor, Alert
from django.utils import timezone
from django import forms
from django.core.exceptions import ValidationError

# Action to mark records as INACTIVE
def mark_inactive(modeladmin, request, queryset):
    updated = queryset.update(status="INACTIVE")
    modeladmin.message_user(request, f"{updated} record(s) marked as INACTIVE")

mark_inactive.short_description = "Mark selected as INACTIVE"

class ZoneInline(admin.TabularInline):
    model = Zone
    extra = 0
    fields = ("name", "status")
    show_change_link = True

class SensorInline(admin.TabularInline):
    model = Sensor
    extra = 0
    fields = ("name", "type", "unit", "status")
    show_change_link = True

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")
    actions = [mark_inactive]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(organization=request.user.userprofile.organization)
        return qs

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")
    actions = [mark_inactive]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(organization=request.user.userprofile.organization)
        return qs

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "zone", "status", "created_at")
    list_filter = ("status", "category", "zone")
    search_fields = ("name", "category__name", "zone__name")
    readonly_fields = ("created_at", "updated_at")
    actions = [mark_inactive]
    list_select_related = ("category", "zone")
    inlines = [SensorInline]
    fieldsets = (
        (None, {"fields": ("name", "reference", "category", "zone", "status")}),
        ("Timestamps", {"fields": ("created_at", "updated_at", "deleted_at")}),
    )

    @admin.action(description="Activar dispositivos seleccionados")
    def make_active(self, request, queryset):
        updated = queryset.update(status="ACTIVE")
        self.message_user(request, f"{updated} dispositivos activados")

    actions.append(make_active)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(organization=request.user.userprofile.organization)
        return qs

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ("id", "device", "value", "unit", "date", "created_at")
    list_filter = ("device", "date")
    search_fields = ("device__name",)
    readonly_fields = ("created_at", "updated_at")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(organization=request.user.userprofile.organization)
        return qs

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("id", "device", "level", "message", "read", "created_at")
    list_filter = ("level", "read")
    search_fields = ("message", "device__name")
    readonly_fields = ("created_at", "updated_at")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(organization=request.user.userprofile.organization)
        return qs

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ("id", "device", "name", "type", "unit", "status", "created_at")
    list_filter = ("type", "status")
    search_fields = ("name", "device__name")
    readonly_fields = ("created_at", "updated_at")
    actions = [mark_inactive]
    list_select_related = ("device",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(organization=request.user.userprofile.organization)
        return qs

# Validación ejemplo para Category
class CategoryForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) > 50:
            raise ValidationError("El nombre no puede tener más de 50 caracteres.")
        return name

# Asignar el formulario con validación a CategoryAdmin
CategoryAdmin.form = CategoryForm
