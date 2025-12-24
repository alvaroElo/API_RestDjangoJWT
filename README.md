# SmartConnect API

> **Sistema de Control de Acceso con RFID**  
> API RESTful desarrollada con Django REST Framework

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-6.0-green.svg)
![DRF](https://img.shields.io/badge/DRF-3.16-red.svg)
![License](https://img.shields.io/badge/License-Educational-yellow.svg)

---

## 📖 Descripción

SmartConnect es un proyecto backend ficticio que simula un sistema de control de acceso mediante sensores RFID. Implementa gestión de usuarios, departamentos, sensores y barreras con autenticación JWT y control de permisos basado en roles.

**⚠️ Proyecto Educativo:** Este es un proyecto completamente ficticio desarrollado con fines de aprendizaje de Django REST Framework, arquitectura de APIs y buenas prácticas de backend. No es un sistema real ni está destinado a uso en producción.

---

## ✨ Características

- 🔐 **Autenticación JWT** con refresh tokens
- 👥 **Sistema de roles** (Admin, Operador, Usuario)
- 📊 **Gestión de departamentos** y barreras
- 🔒 **Permisos granulares** por endpoint
- 📝 **API RESTful** completa con CRUD
- 🗄️ **Soporte MySQL y SQLite**

---

## 🛠️ Tecnologías

- **Backend:** Django 6.0
- **API:** Django REST Framework 3.16
- **Autenticación:** Simple JWT 5.5
- **Base de datos:** MySQL 8.0+ / SQLite
- **CORS:** django-cors-headers
- **Variables de entorno:** python-dotenv

---

## 🚀 Instalación

### Requisitos previos
- Python 3.10+
- MySQL 8.0+ o WampServer (opcional: SQLite)

### Instalación rápida

```bash
# Clonar repositorio
git clone <url-del-repositorio>
cd lilisProject

# Crear entorno virtual
python -m venv venv
venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
copy .env.exampleAPI .env
# Editar .env con tus credenciales

# Crear base de datos y migrar
python manage.py migrate

# Crear datos de prueba
python scripts/crear_datos_iniciales.py

# Iniciar servidor
python manage.py runserver
```

📘 Ver guía completa: [INSTALACION.MD](INSTALACION.MD)

---

## 🔗 Endpoints Principales

**Base URL:** `http://localhost:8000`

### Autenticación
- `POST /api/token/` - Obtener token JWT
- `POST /api/token/refresh/` - Renovar token

### Recursos
- `GET|POST /api/usuarios/` - Gestión de usuarios
- `GET|POST /api/departamentos/` - Gestión de departamentos
- `GET|POST /api/sensores/` - Gestión de sensores RFID
- `GET|POST /api/barreras/` - Gestión de barreras

### Acciones
- `POST /api/sensores/{id}/activar/` - Activar sensor
- `POST /api/barreras/{id}/abrir/` - Abrir barrera
- `POST /api/barreras/{id}/cerrar/` - Cerrar barrera

📚 Ver documentación completa: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

## 📁 Estructura del Proyecto

```
lilisProject/
├── access_control/          # App principal
│   ├── models.py           # Modelos (Usuario, Sensor, Barrera, etc.)
│   ├── views.py            # Vistas/ViewSets
│   ├── serializers.py      # Serializadores DRF
│   ├── permissions.py      # Permisos personalizados
│   └── urls.py             # URLs de la app
├── smartconnect/           # Configuración
│   ├── settings.py         # Settings principal
│   └── urls.py             # URLs raíz
├── scripts/                # Scripts auxiliares
│   └── crear_datos_iniciales.py
├── .env.exampleAPI         # Ejemplo de configuración
├── requirements.txt        # Dependencias
└── manage.py              # CLI Django
```

---

## 🔑 Credenciales de Prueba

Después de ejecutar `crear_datos_iniciales.py`:

```
Admin:
  Usuario: admin
  Password: admin123

Operador:
  Usuario: operador
  Password: operador123
```

---

## 🧪 Ejemplo de Uso

### Obtener token JWT

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### Listar usuarios (requiere token)

```bash
curl -X GET http://localhost:8000/api/usuarios/ \
  -H "Authorization: Bearer <tu_token>"
```

### Activar sensor RFID

```bash
curl -X POST http://localhost:8000/api/sensores/1/activar/ \
  -H "Authorization: Bearer <tu_token>"
```

---

## 🎓 Propósito Educativo

Este proyecto fue desarrollado para aprender:

- ✅ Arquitectura de APIs RESTful
- ✅ Autenticación y autorización con JWT
- ✅ Django REST Framework
- ✅ Modelos relacionales complejos
- ✅ Sistema de permisos y roles
- ✅ Buenas prácticas de seguridad
- ✅ Documentación de APIs

**Nota:** Las credenciales y configuraciones son simplificadas para facilitar el aprendizaje. Un sistema de producción requeriría medidas de seguridad adicionales.

---

## 🔒 Seguridad

### Implementado
- ✅ Autenticación JWT
- ✅ Permisos por rol
- ✅ Variables de entorno para secretos
- ✅ Validación de datos

### Para producción (no implementado)
- ⚠️ Rate limiting
- ⚠️ Autenticación 2FA
- ⚠️ HTTPS obligatorio
- ⚠️ Auditoría de logs
- ⚠️ Contraseñas seguras

---

## 📝 Comandos Útiles

```bash
# Crear superusuario
python manage.py createsuperuser

# Ejecutar tests
python manage.py test

# Acceder al shell de Django
python manage.py shell

# Panel de administración
http://localhost:8000/admin/
```

---

## 📄 Licencia

Proyecto de código abierto con fines educativos.

---

## 👤 Autor

**Alvaro Elo [ALZOR]**

Proyecto desarrollado como parte del aprendizaje de desarrollo backend con Django y APIs RESTful.

---

⭐ Si este proyecto te ayudó en tu aprendizaje, considera darle una estrella
