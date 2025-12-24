from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator


class Usuario(AbstractUser):
    """
    Modelo de Usuario personalizado que extiende AbstractUser
    Roles: ADMIN, OPERADOR
    """
    class Rol(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        OPERADOR = 'OPERADOR', 'Operador'

    rol = models.CharField(
        max_length=10,
        choices=Rol.choices,
        default=Rol.OPERADOR,
        verbose_name='Rol'
    )
    telefono = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Teléfono'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"

    def es_admin(self):
        """Verifica si el usuario es administrador"""
        return self.rol == self.Rol.ADMIN


class Departamento(models.Model):
    """
    Modelo de Departamento o Zona
    Representa espacios físicos o áreas en la empresa
    """
    nombre = models.CharField(
        max_length=100,
        unique=True,
        validators=[MinLengthValidator(3)],
        verbose_name='Nombre'
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )
    ubicacion = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Ubicación'
    )
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Sensor(models.Model):
    """
    Modelo de Sensor RFID
    Representa tarjetas o llaveros RFID
    """
    class Estado(models.TextChoices):
        ACTIVO = 'ACTIVO', 'Activo'
        INACTIVO = 'INACTIVO', 'Inactivo'
        BLOQUEADO = 'BLOQUEADO', 'Bloqueado'
        PERDIDO = 'PERDIDO', 'Perdido'

    uid_mac = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='UID/MAC'
    )
    nombre = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)],
        verbose_name='Nombre'
    )
    estado = models.CharField(
        max_length=10,
        choices=Estado.choices,
        default=Estado.ACTIVO,
        verbose_name='Estado'
    )
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sensores',
        verbose_name='Departamento'
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sensores',
        verbose_name='Usuario asignado'
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')

    class Meta:
        verbose_name = 'Sensor'
        verbose_name_plural = 'Sensores'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nombre} ({self.uid_mac})"

    def esta_activo(self):
        """Verifica si el sensor está activo"""
        return self.estado == self.Estado.ACTIVO


class Barrera(models.Model):
    """
    Modelo de Barrera de acceso
    Representa el estado de la barrera de acceso
    """
    class Estado(models.TextChoices):
        ABIERTA = 'ABIERTA', 'Abierta'
        CERRADA = 'CERRADA', 'Cerrada'

    nombre = models.CharField(
        max_length=100,
        unique=True,
        validators=[MinLengthValidator(3)],
        verbose_name='Nombre'
    )
    estado = models.CharField(
        max_length=10,
        choices=Estado.choices,
        default=Estado.CERRADA,
        verbose_name='Estado'
    )
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.CASCADE,
        related_name='barreras',
        verbose_name='Departamento'
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')

    class Meta:
        verbose_name = 'Barrera'
        verbose_name_plural = 'Barreras'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} - {self.get_estado_display()}"

    def abrir(self):
        """Abre la barrera"""
        self.estado = self.Estado.ABIERTA
        self.save()

    def cerrar(self):
        """Cierra la barrera"""
        self.estado = self.Estado.CERRADA
        self.save()

    def esta_abierta(self):
        """Verifica si la barrera está abierta"""
        return self.estado == self.Estado.ABIERTA


class Evento(models.Model):
    """
    Modelo de Evento de acceso
    Registra todos los intentos de acceso y acciones sobre las barreras
    """
    class TipoEvento(models.TextChoices):
        ACCESO_PERMITIDO = 'ACCESO_PERMITIDO', 'Acceso Permitido'
        ACCESO_DENEGADO = 'ACCESO_DENEGADO', 'Acceso Denegado'
        APERTURA_MANUAL = 'APERTURA_MANUAL', 'Apertura Manual'
        CIERRE_MANUAL = 'CIERRE_MANUAL', 'Cierre Manual'

    tipo = models.CharField(
        max_length=20,
        choices=TipoEvento.choices,
        verbose_name='Tipo de evento'
    )
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='eventos',
        verbose_name='Sensor'
    )
    barrera = models.ForeignKey(
        Barrera,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='eventos',
        verbose_name='Barrera'
    )
    usuario_responsable = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='eventos_realizados',
        verbose_name='Usuario responsable'
    )
    motivo_denegacion = models.TextField(
        blank=True,
        verbose_name='Motivo de denegación'
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y hora')

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
