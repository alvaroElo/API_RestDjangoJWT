# Instalación - SmartConnect API

> **⚠️ Proyecto educativo** - Credenciales de ejemplo incluidas para desarrollo local únicamente.

---

## Requisitos

- Python 3.10+
- MySQL 8.0+ o WampServer (opcional: SQLite para pruebas rápidas)

---

## Instalación Rápida

### 1. Configurar entorno

```bash
# Clonar y entrar al proyecto
git clone <url-del-repositorio>
cd lilisProject

# Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar base de datos

**Opción A - MySQL/WampServer:**

```sql
CREATE DATABASE api_rest_az CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'az_user'@'localhost' IDENTIFIED BY 'az_password123';
GRANT ALL PRIVILEGES ON api_rest_az.* TO 'az_user'@'localhost';
FLUSH PRIVILEGES;
```

Copia y configura el archivo `.env`:
```bash
copy .env.exampleAPI .env
```

Edita `.env` con tus credenciales:
```bash
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=genera_una_clave_con_el_comando_abajo
DB_ENGINE=mysql
DB_NAME=api_rest_az
DB_USER=az_user
DB_PASSWORD=az_password123
DB_HOST=localhost
```

Generar SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Opción B - SQLite (más simple):**

En tu `.env`:
```bash
DB_ENGINE=sqlite
```

### 3. Inicializar Django

```bash
# Crear y aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# Crear datos de prueba (usuarios, sensores, barreras)
python scripts/crear_datos_iniciales.py

# Iniciar servidor
python manage.py runserver
```

---

## Probar la API

- **Servidor:** http://localhost:8000
- **Admin:** http://localhost:8000/admin/
- **Token JWT:** http://localhost:8000/api/token/
- **Refresh Token:** http://localhost:8000/api/token/refresh/
- **Usuarios:** http://localhost:8000/api/usuarios/
- **Departamentos:** http://localhost:8000/api/departamentos/
- **Sensores:** http://localhost:8000/api/sensores/
- **Barreras:** http://localhost:8000/api/barreras/
- **Documentación completa:** [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

## Comandos Útiles

```bash
python manage.py createsuperuser        # Crear admin adicional
python manage.py test                   # Ejecutar tests
```

Panel de administración: http://localhost:8000/admin/

---

## Solución de Problemas

**"No module named 'rest_framework'"**  
→ Activa el entorno virtual: `.venv\Scripts\Activate.ps1`

**"Access denied" en MySQL**  
→ Verifica credenciales en `.env` y permisos del usuario

**"Can't connect to MySQL server"**  
→ Asegúrate que WampServer/MySQL esté corriendo

---

**Autor:** Alvaro Elo [ALZOR] | Proyecto educativo Django REST Framework