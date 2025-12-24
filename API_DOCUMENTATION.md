# API SmartConnect - Documentación de Endpoints

## Base URL
```
http://localhost:8000/api/
```

## Autenticación

### 1. Obtener Token JWT
**POST** `/api/token/`

**Body:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Respuesta:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 2. Refrescar Token
**POST** `/api/token/refresh/`

**Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## Endpoints Públicos

### Información del Proyecto
**GET** `/api/info/`

No requiere autenticación.

**Respuesta:**
```json
{
  "autor": ["Alvaro Elo [ALZOR]"],
  "area": "Programación Back End",
  "proyecto": "ApiRest SmartConnect",
  "descripcion": "API RESTful desarrollada de forma autónoma con Django REST Framework, implementando autenticación segura mediante JWT",
  "version": "1.0"
}
```

## Endpoints Protegidos

**Nota:** Todos los endpoints siguientes requieren el header:
```
Authorization: Bearer <access_token>
```

### Usuarios

#### Listar usuarios
**GET** `/api/usuarios/`

#### Obtener usuario por ID
**GET** `/api/usuarios/{id}/`

#### Crear usuario (Solo Admin)
**POST** `/api/usuarios/`

**Body:**
```json
{
  "username": "nuevo_usuario",
  "email": "usuario@example.com",
  "password": "password123",
  "first_name": "Nombre",
  "last_name": "Apellido",
  "rol": "OPERADOR",
  "telefono": "+56912345678"
}
```

#### Actualizar usuario (Solo Admin)
**PUT/PATCH** `/api/usuarios/{id}/`

#### Eliminar usuario (Solo Admin)
**DELETE** `/api/usuarios/{id}/`

---

### Departamentos

#### Listar departamentos
**GET** `/api/departamentos/`

#### Obtener departamento por ID
**GET** `/api/departamentos/{id}/`

#### Crear departamento (Solo Admin)
**POST** `/api/departamentos/`

**Body:**
```json
{
  "nombre": "Nombre Departamento",
  "descripcion": "Descripción del departamento",
  "ubicacion": "Ubicación física",
  "activo": true
}
```

#### Actualizar departamento (Solo Admin)
**PUT/PATCH** `/api/departamentos/{id}/`

#### Eliminar departamento (Solo Admin)
**DELETE** `/api/departamentos/{id}/`

---

### Sensores

#### Listar sensores
**GET** `/api/sensores/`

#### Obtener sensor por ID
**GET** `/api/sensores/{id}/`

#### Crear sensor (Solo Admin)
**POST** `/api/sensores/`

**Body:**
```json
{
  "uid_mac": "RFID-004-DDD",
  "nombre": "Tarjeta Nueva",
  "estado": "ACTIVO",
  "departamento": 1,
  "usuario": 2,
  "descripcion": "Descripción del sensor"
}
```

**Estados válidos:** `ACTIVO`, `INACTIVO`, `BLOQUEADO`, `PERDIDO`

#### Actualizar sensor (Solo Admin)
**PUT/PATCH** `/api/sensores/{id}/`

#### Eliminar sensor (Solo Admin)
**DELETE** `/api/sensores/{id}/`

#### Activar sensor (Solo Admin)
**POST** `/api/sensores/{id}/activar/`

#### Desactivar sensor (Solo Admin)
**POST** `/api/sensores/{id}/desactivar/`

#### Verificar acceso
**POST** `/api/sensores/verificar_acceso/`

Simula el flujo de validación de acceso de un sensor RFID.

**Body:**
```json
{
  "uid_mac": "RFID-001-AAA",
  "barrera_id": 1
}
```

**Respuesta exitosa:**
```json
{
  "acceso": "permitido",
  "sensor": {
    "id": 1,
    "nombre": "Tarjeta Admin Principal",
    "uid_mac": "RFID-001-AAA",
    "estado": "ACTIVO",
    ...
  },
  "mensaje": "Acceso concedido"
}
```

**Respuesta denegada:**
```json
{
  "acceso": "denegado",
  "motivo": "Sensor en estado: Inactivo",
  "sensor": {...}
}
```

---

### Barreras

#### Listar barreras
**GET** `/api/barreras/`

#### Obtener barrera por ID
**GET** `/api/barreras/{id}/`

#### Crear barrera (Solo Admin)
**POST** `/api/barreras/`

**Body:**
```json
{
  "nombre": "Barrera Nueva",
  "estado": "CERRADA",
  "departamento": 1,
  "descripcion": "Descripción de la barrera"
}
```

**Estados válidos:** `ABIERTA`, `CERRADA`

#### Actualizar barrera (Solo Admin)
**PUT/PATCH** `/api/barreras/{id}/`

#### Eliminar barrera (Solo Admin)
**DELETE** `/api/barreras/{id}/`

#### Abrir barrera
**POST** `/api/barreras/{id}/abrir/`

Abre la barrera manualmente y registra un evento.

**Respuesta:**
```json
{
  "status": "barrera abierta",
  "barrera": {
    "id": 1,
    "nombre": "Barrera Principal",
    "estado": "ABIERTA",
    ...
  }
}
```

#### Cerrar barrera
**POST** `/api/barreras/{id}/cerrar/`

Cierra la barrera manualmente y registra un evento.

---

### Eventos

Los eventos son de solo lectura y se generan automáticamente.

#### Listar eventos
**GET** `/api/eventos/`

#### Obtener evento por ID
**GET** `/api/eventos/{id}/`

**Tipos de eventos:**
- `ACCESO_PERMITIDO`
- `ACCESO_DENEGADO`
- `APERTURA_MANUAL`
- `CIERRE_MANUAL`

---

## Permisos

### Administrador (rol: ADMIN)
- CRUD completo en todas las entidades
- Puede activar/desactivar sensores
- Puede abrir/cerrar barreras
- Puede crear usuarios y asignar roles

### Operador (rol: OPERADOR)
- Solo lectura (GET) en todas las entidades
- Puede abrir/cerrar barreras
- Puede verificar acceso de sensores
- No puede crear, actualizar o eliminar

---

## Códigos de Estado HTTP

- `200 OK` - Solicitud exitosa
- `201 Created` - Recurso creado exitosamente
- `204 No Content` - Eliminación exitosa
- `400 Bad Request` - Error de validación
- `401 Unauthorized` - No autenticado
- `403 Forbidden` - Sin permisos
- `404 Not Found` - Recurso no encontrado
- `405 Method Not Allowed` - Método no permitido

---

## Credenciales de Prueba

### Administrador
```
username: admin
password: admin123
```

### Operador
```
username: operador
password: operador123
```

### Sensores RFID de Prueba
```
RFID-001-AAA - Tarjeta Admin Principal (ACTIVO)
RFID-002-BBB - Tarjeta Operador Juan (ACTIVO)
RFID-003-CCC - Tarjeta Almacén (INACTIVO)
```

---

## Ejemplo de Flujo Completo

### 1. Autenticarse
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### 2. Listar sensores
```bash
curl -X GET http://localhost:8000/api/sensores/ \
  -H "Authorization: Bearer <access_token>"
```

### 3. Verificar acceso de un sensor
```bash
curl -X POST http://localhost:8000/api/sensores/verificar_acceso/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"uid_mac": "RFID-001-AAA", "barrera_id": 1}'
```

### 4. Abrir barrera manualmente
```bash
curl -X POST http://localhost:8000/api/barreras/1/abrir/ \
  -H "Authorization: Bearer <access_token>"
```

### 5. Ver eventos registrados
```bash
curl -X GET http://localhost:8000/api/eventos/ \
  -H "Authorization: Bearer <access_token>"
```
