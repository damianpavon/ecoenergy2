def run():
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from usuarios.models import Module, Role, RoleModulePermission
    from dispositivos.models import Category, Zone, Device, Measurement, Sensor, Alert
    from usuarios.models import Organization, UserProfile

    def create_modules():
        modules_data = [
            {'code': 'dispositivos', 'name': 'Dispositivos'},
            {'code': 'usuarios', 'name': 'Usuarios'},
        ]
        for data in modules_data:
            Module.objects.get_or_create(**data)
        print("Módulos creados")

    def create_roles():
        roles_data = [
            {'name': 'Admin'},
            {'name': 'Manager'},
            {'name': 'User'},
        ]
        for data in roles_data:
            group, created = Group.objects.get_or_create(name=data['name'])
            Role.objects.get_or_create(group=group)
        print("Roles creados")

    def create_permissions():
        # Obtener roles
        admin_role = Role.objects.get(group__name='Admin')
        manager_role = Role.objects.get(group__name='Manager')
        user_role = Role.objects.get(group__name='User')

        # Obtener módulos
        dispositivos_module = Module.objects.get(code='dispositivos')
        usuarios_module = Module.objects.get(code='usuarios')

        # Permisos para Admin: todos en ambos módulos
        RoleModulePermission.objects.get_or_create(
            role=admin_role, module=dispositivos_module,
            defaults={'can_view': True, 'can_add': True, 'can_change': True, 'can_delete': True}
        )
        RoleModulePermission.objects.get_or_create(
            role=admin_role, module=usuarios_module,
            defaults={'can_view': True, 'can_add': True, 'can_change': True, 'can_delete': True}
        )

        # Permisos para Manager: view, add, change en dispositivos; view en usuarios
        RoleModulePermission.objects.get_or_create(
            role=manager_role, module=dispositivos_module,
            defaults={'can_view': True, 'can_add': True, 'can_change': True, 'can_delete': False}
        )
        RoleModulePermission.objects.get_or_create(
            role=manager_role, module=usuarios_module,
            defaults={'can_view': True, 'can_add': False, 'can_change': False, 'can_delete': False}
        )

        # Permisos para User: view en dispositivos; ninguno en usuarios
        RoleModulePermission.objects.get_or_create(
            role=user_role, module=dispositivos_module,
            defaults={'can_view': True, 'can_add': False, 'can_change': False, 'can_delete': False}
        )
        RoleModulePermission.objects.get_or_create(
            role=user_role, module=usuarios_module,
            defaults={'can_view': False, 'can_add': False, 'can_change': False, 'can_delete': False}
        )

        print("Permisos de roles creados")

    def assign_django_permissions():
        # Modelos de dispositivos
        dispositivos_models = [Category, Zone, Device, Measurement, Sensor, Alert]
        # Modelos de usuarios
        usuarios_models = [Organization, UserProfile]

        # Obtener grupos
        admin_group = Group.objects.get(name='Admin')
        manager_group = Group.objects.get(name='Manager')
        user_group = Group.objects.get(name='User')

        # Asignar permisos a Admin: todos en todos los modelos
        for model in dispositivos_models + usuarios_models:
            ct = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(content_type=ct)
            admin_group.permissions.add(*perms)

        # Asignar permisos a Manager: view, add, change en dispositivos; view en usuarios
        for model in dispositivos_models:
            ct = ContentType.objects.get_for_model(model)
            view_perm = Permission.objects.get(content_type=ct, codename=f'view_{model._meta.model_name}')
            add_perm = Permission.objects.get(content_type=ct, codename=f'add_{model._meta.model_name}')
            change_perm = Permission.objects.get(content_type=ct, codename=f'change_{model._meta.model_name}')
            manager_group.permissions.add(view_perm, add_perm, change_perm)

        for model in usuarios_models:
            ct = ContentType.objects.get_for_model(model)
            view_perm = Permission.objects.get(content_type=ct, codename=f'view_{model._meta.model_name}')
            manager_group.permissions.add(view_perm)

        # Asignar permisos a User: view en dispositivos
        for model in dispositivos_models:
            ct = ContentType.objects.get_for_model(model)
            view_perm = Permission.objects.get(content_type=ct, codename=f'view_{model._meta.model_name}')
            user_group.permissions.add(view_perm)

        print("Permisos de Django asignados a grupos")

    create_modules()
    create_roles()
    create_permissions()
    assign_django_permissions()
    print("Semilla completada")

if __name__ == '__main__':
    import django
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoreo.settings')
    django.setup()
    run()
