# -*- coding: utf-8 -*-
"""
Script para crear datos iniciales de prueba
"""
import os
import sys
import django

# Agregar el directorio raíz del proyecto al path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# 1. Configurar el entorno de Django
# IMPORTANTE: El nombre del proyecto dentro de settings.py es 'smartconnect'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartconnect.settings')

# 2. Inicializar Django
django.setup()

# 3. Importar modelos (esto debe ir DESPUÉS de django.setup)
from access_control.models import Usuario, Departamento, Sensor, Barrera

def main():
    print("=== Iniciando creación de datos ===")

    # --- Crear Usuarios ---
    print("\nCreando usuarios...")
    
    # Admin
    if not Usuario.objects.filter(username='admin').exists():
        admin = Usuario.objects.create_user(
            username='admin',
            email='admin@smartconnect.com',
            password='admin123',
            rol=Usuario.Rol.ADMIN,
            first_name='Admin',
            last_name='SmartConnect',
            is_staff=True,
            is_superuser=True
        )
        print(f"✓ Usuario Admin creado: {admin.username}")
    else:
        admin = Usuario.objects.get(username='admin')
        print(f"! El usuario Admin ya existía.")

    # Operador
    if not Usuario.objects.filter(username='operador').exists():
        operador = Usuario.objects.create_user(
            username='operador',
            email='operador@smartconnect.com',
            password='operador123',
            rol=Usuario.Rol.OPERADOR,
            first_name='Juan',
            last_name='Pérez'
        )
        print(f"✓ Usuario Operador creado: {operador.username}")
    else:
        operador = Usuario.objects.get(username='operador')
        print(f"! El usuario Operador ya existía.")

    # --- Crear Departamentos ---
    print("\nCreando departamentos...")
    
    recepcion, _ = Departamento.objects.get_or_create(
        nombre='Recepción',
        defaults={
            'descripcion': 'Área de recepción principal',
            'ubicacion': 'Planta baja'
        }
    )
    print(f"✓ Departamento: {recepcion.nombre}")

    oficinas, _ = Departamento.objects.get_or_create(
        nombre='Oficinas Administrativas',
        defaults={
            'descripcion': 'Oficinas del personal administrativo',
            'ubicacion': 'Segundo piso'
        }
    )
    print(f"✓ Departamento: {oficinas.nombre}")

    almacen, _ = Departamento.objects.get_or_create(
        nombre='Almacén',
        defaults={
            'descripcion': 'Área de almacenamiento',
            'ubicacion': 'Planta baja, sector norte'
        }
    )
    print(f"✓ Departamento: {almacen.nombre}")

    # --- Crear Sensores ---
    print("\nCreando sensores...")
    
    sensor1, _ = Sensor.objects.get_or_create(
        uid_mac='RFID-001-AAA',
        defaults={
            'nombre': 'Tarjeta Admin Principal',
            'estado': Sensor.Estado.ACTIVO,
            'departamento': recepcion,
            'usuario': admin,
            'descripcion': 'Tarjeta maestra del administrador'
        }
    )
    print(f"✓ Sensor: {sensor1.nombre}")

    sensor2, _ = Sensor.objects.get_or_create(
        uid_mac='RFID-002-BBB',
        defaults={
            'nombre': 'Tarjeta Operador Juan',
            'estado': Sensor.Estado.ACTIVO,
            'departamento': oficinas,
            'usuario': operador,
            'descripcion': 'Tarjeta de acceso del operador Juan Pérez'
        }
    )
    print(f"✓ Sensor: {sensor2.nombre}")

    sensor3, _ = Sensor.objects.get_or_create(
        uid_mac='RFID-003-CCC',
        defaults={
            'nombre': 'Tarjeta Almacén',
            'estado': Sensor.Estado.INACTIVO,
            'departamento': almacen,
            'descripcion': 'Tarjeta de acceso al almacén (desactivada temporalmente)'
        }
    )
    print(f"✓ Sensor: {sensor3.nombre}")

    # --- Crear Barreras ---
    print("\nCreando barreras...")
    
    barrera1, _ = Barrera.objects.get_or_create(
        nombre='Barrera Principal',
        defaults={
            'estado': Barrera.Estado.CERRADA,
            'departamento': recepcion,
            'descripcion': 'Barrera de acceso principal al edificio'
        }
    )
    print(f"✓ Barrera: {barrera1.nombre}")

    barrera2, _ = Barrera.objects.get_or_create(
        nombre='Barrera Almacén',
        defaults={
            'estado': Barrera.Estado.CERRADA,
            'departamento': almacen,
            'descripcion': 'Barrera de acceso al área de almacén'
        }
    )
    print(f"✓ Barrera: {barrera2.nombre}")

    # --- Resumen Final ---
    print("\n" + "="*50)
    print("✓ PROCESO COMPLETADO EXITOSAMENTE")
    print("="*50)
    print("Credenciales de prueba:")
    print(f"  Admin    -> User: admin    | Pass: admin123")
    print(f"  Operador -> User: operador | Pass: operador123")

if __name__ == '__main__':
    main()