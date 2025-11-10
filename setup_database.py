#!/usr/bin/env python
"""
Script para configurar la base de datos PostgreSQL o MySQL para el proyecto EcoEnergy.

Este script:
1. Crea la base de datos si no existe
2. Ejecuta las migraciones de Django
3. Pobla la base de datos con datos de ejemplo

Uso:
    python setup_database.py [postgresql|mysql]
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, cwd=None):
    """Ejecuta un comando y retorna el resultado."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando comando: {command}")
        print(f"Error: {e.stderr}")
        return None

def setup_postgresql():
    """Configura PostgreSQL."""
    print("🔧 Configurando PostgreSQL...")

    # Verificar si PostgreSQL está instalado
    if not run_command("psql --version"):
        print("❌ PostgreSQL no está instalado.")
        print("📦 Instala PostgreSQL desde: https://www.postgresql.org/download/")
        return False

    # Crear base de datos
    db_name = os.environ.get('DATABASE_NAME', 'ecoenergy_db')
    db_user = os.environ.get('DATABASE_USER', 'postgres')

    print(f"📦 Creando base de datos '{db_name}'...")

    # Comando para crear la base de datos
    create_db_command = f'psql -U {db_user} -c "CREATE DATABASE {db_name} WITH ENCODING \'UTF8\';"'

    result = run_command(create_db_command)
    if result is None:
        print("⚠️  La base de datos ya existe o no se pudo crear.")
        print("   Asegúrate de que el usuario tenga permisos para crear bases de datos.")

    return True

def setup_mysql():
    """Configura MySQL."""
    print("🔧 Configurando MySQL...")

    # Verificar si MySQL está instalado
    if not run_command("mysql --version"):
        print("❌ MySQL no está instalado.")
        print("📦 Instala MySQL desde: https://dev.mysql.com/downloads/mysql/")
        return False

    # Crear base de datos
    db_name = os.environ.get('DATABASE_NAME', 'ecoenergy_db')
    db_user = os.environ.get('DATABASE_USER', 'root')
    db_password = os.environ.get('DATABASE_PASSWORD', '')

    print(f"📦 Creando base de datos '{db_name}'...")

    # Comando para crear la base de datos
    password_option = f"-p{db_password}" if db_password else ""
    create_db_command = f'mysql -u {db_user} {password_option} -e "CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"'

    result = run_command(create_db_command)
    if result is None:
        print("❌ Error creando la base de datos MySQL.")
        print("   Verifica tus credenciales y permisos.")
        return False

    return True

def run_migrations():
    """Ejecuta las migraciones de Django."""
    print("🔄 Ejecutando migraciones de Django...")

    # Ejecutar makemigrations
    print("   Creando migraciones...")
    result = run_command("python manage.py makemigrations")
    if result is not None:
        print("   ✅ Migraciones creadas")

    # Ejecutar migrate
    print("   Aplicando migraciones...")
    result = run_command("python manage.py migrate")
    if result is not None:
        print("   ✅ Migraciones aplicadas")
    else:
        print("   ❌ Error aplicando migraciones")
        return False

    return True

def populate_database():
    """Pobla la base de datos con datos de ejemplo."""
    print("📊 Poblando base de datos con datos de ejemplo...")

    # Ejecutar script de población
    scripts = [
        'populate_data.py',
        'populate_organization_user.py',
        'seed_roles_permissions.py'
    ]

    for script in scripts:
        if os.path.exists(script):
            print(f"   Ejecutando {script}...")
            result = run_command(f"python {script}")
            if result is not None:
                print(f"   ✅ {script} ejecutado")
            else:
                print(f"   ⚠️  Error ejecutando {script}")
        else:
            print(f"   ⚠️  {script} no encontrado")

def main():
    if len(sys.argv) != 2:
        print("Uso: python setup_database.py [postgresql|mysql]")
        print("\nEjemplos:")
        print("  python setup_database.py postgresql")
        print("  python setup_database.py mysql")
        sys.exit(1)

    db_type = sys.argv[1].lower()

    if db_type not in ['postgresql', 'mysql']:
        print("❌ Tipo de base de datos no válido. Usa 'postgresql' o 'mysql'.")
        sys.exit(1)

    # Verificar que existe el archivo .env
    if not os.path.exists('.env'):
        print("❌ Archivo .env no encontrado.")
        print("📋 Copia .env.example a .env y configura tus variables de base de datos:")
        print("   cp .env.example .env")
        sys.exit(1)

    # Cargar variables de entorno
    from dotenv import load_dotenv
    load_dotenv()

    print("🚀 Configurando base de datos para EcoEnergy...")
    print(f"📍 Tipo de BD: {db_type.upper()}")

    # Configurar base de datos
    if db_type == 'postgresql':
        success = setup_postgresql()
    else:
        success = setup_mysql()

    if not success:
        print("❌ Error configurando la base de datos.")
        sys.exit(1)

    # Ejecutar migraciones
    if not run_migrations():
        print("❌ Error ejecutando migraciones.")
        sys.exit(1)

    # Poblar base de datos
    populate_database()

    print("\n✅ Configuración completada!")
    print("\n🎯 Para usar el proyecto:")
    print("   python manage.py runserver")
    print("\n🔑 Credenciales de prueba:")
    print("   Admin: admin / admin123")
    print("   Manager: manager_user / manager123")
    print("   User: user_user / user123")
    print("   Test: test@example.com / test123")

if __name__ == '__main__':
    main()
