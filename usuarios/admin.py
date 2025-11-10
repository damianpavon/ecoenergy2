from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Organization, UserProfile, Module, Role, RoleModulePermission
from django.utils import timezone
from django import forms
from django.core.exceptions import ValidationError

# Action to mark records as INACTIVE
def mark_inactive(modeladmin, request, queryset):
    updated = queryset.update(status="INACTIVE")
    modeladmin.message_user(request, f"{updated} registro(s) marcado(s) como INACTIVO")

mark_inactive.short_description = "Marcar seleccionados como INACTIVOS"

# Inline for RoleModulePermission
class RoleModulePermissionInline(admin.TabularInline):
    model = RoleModulePermission
    extra = 0
    fields = ("module", "can_view", "can_add", "can_change", "can_delete")

# Form with validation for Organization
class OrganizationForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) > 100:
            raise ValidationError("El nombre no puede tener más de 100 caracteres.")
        return name

# Register Organization
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name", "email")
    readonly_fields = ("created_at", "updated_at")
    form = OrganizationForm
    actions = [mark_inactive]
    ordering = ("-created_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            try:
                qs = qs.filter(id=request.user.userprofile.organization.id)
            except AttributeError:
                qs = qs.none()
        return qs

# Inline for UserProfile (but since OneToOne, perhaps not needed, but for completeness)
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 0
    fields = ("organization", "rut", "telefono", "direccion")

# Extend UserAdmin to include UserProfile
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

# Unregister default User and register custom
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "organization", "rut", "telefono", "direccion")
    list_filter = ("organization",)
    search_fields = ("user__username", "user__email", "rut")
    list_select_related = ("user", "organization")
    ordering = ("user__username",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            try:
                qs = qs.filter(organization=request.user.userprofile.organization)
            except AttributeError:
                qs = qs.none()
        return qs

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "icon")
    search_fields = ("name", "code")
    ordering = ("name",)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id", "group")
    search_fields = ("group__name",)
    inlines = [RoleModulePermissionInline]
    ordering = ("group__name",)

@admin.register(RoleModulePermission)
class RoleModulePermissionAdmin(admin.ModelAdmin):
    list_display = ("id", "role", "module", "can_view", "can_add", "can_change", "can_delete")
    list_filter = ("role", "module", "can_view", "can_add", "can_change", "can_delete")
    search_fields = ("role__group__name", "module__name")
    list_select_related = ("role", "module")
    ordering = ("role__group__name",)
