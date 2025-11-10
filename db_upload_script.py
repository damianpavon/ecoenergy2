import os
import django
from django.conf import settings
from django.core import management

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoreo.settings')
django.setup()

def dump_database(filename='data_backup.json'):
    """
    Exporta todos los datos de la base de datos a un archivo JSON.
    Uso: dump_database('mi_backup.json')
    """
    try:
        management.call_command('dumpdata', '--natural-foreign', '--natural-primary', '-e', 'auth.permission', '-e', 'contenttypes', '--indent=2', 'usuarios', 'dispositivos', stdout=open(filename, 'w'))
        print(f"Datos exportados exitosamente a {filename}")
    except Exception as e:
        print(f"Error al exportar: {e}")

def load_database(filename='data_backup.json'):
    """
    Carga datos desde un archivo JSON a la base de datos.
    Uso: load_database('mi_backup.json')
    Asegúrate de que las migraciones estén aplicadas primero.
    """
    try:
        management.call_command('loaddata', filename)
        print(f"Datos cargados exitosamente desde {filename}")
    except Exception as e:
        print(f"Error al cargar: {e}")

def full_backup_and_upload():
    """
    Realiza un backup completo y simula upload (puedes agregar código para subir a cloud, e.g., AWS S3 o GitHub).
    Para upload real, instala boto3 para S3 o usa git push.
    """
    dump_filename = 'full_backup.json'
    dump_database(dump_filename)
    
    # Ejemplo: Subir a GitHub o servidor (ajusta según tu setup)
    # os.system('git add full_backup.json && git commit -m "Backup DB" && git push')
    
    print("Backup completado. Para subir: Copia full_backup.json a tu servidor y ejecuta load_database allí.")
    print("En servidor remoto: python manage.py migrate && python db_upload_script.py load_database('full_backup.json')")

if __name__ == '__main__':
    # Ejemplo de uso: full_backup_and_upload()
    pass
