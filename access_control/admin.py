from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Departamento, Sensor, Barrera, Evento


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'rol', 'first_name', 'last_name', 'is_active']
    list_filter = ['rol', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('rol', 'telefono')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('rol', 'telefono')}),
    )


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ubicacion', 'activo', 'created_at']
    list_filter = ['activo', 'created_at']
    search_fields = ['nombre', 'ubicacion', 'descripcion']


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'uid_mac', 'estado', 'departamento', 'usuario', 'created_at']
    list_filter = ['estado', 'departamento', 'created_at']
    search_fields = ['nombre', 'uid_mac', 'descripcion']
    raw_id_fields = ['usuario', 'departamento']


@admin.register(Barrera)
class BarreraAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'estado', 'departamento', 'created_at']
    list_filter = ['estado', 'departamento', 'created_at']
    search_fields = ['nombre', 'descripcion']
    raw_id_fields = ['departamento']


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'sensor', 'barrera', 'usuario_responsable', 'timestamp']
    list_filter = ['tipo', 'timestamp', 'barrera']
    search_fields = ['descripcion', 'motivo_denegacion']
    raw_id_fields = ['sensor', 'barrera', 'usuario_responsable']
    readonly_fields = ['timestamp']
