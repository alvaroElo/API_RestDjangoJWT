from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Usuario, Departamento, Sensor, Barrera, Evento
from .serializers import (
    UsuarioSerializer, DepartamentoSerializer, SensorSerializer,
    BarreraSerializer, EventoSerializer
)
from .permissions import IsAdminOrReadOnly, IsAdmin


@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """
    Endpoint /api/info/ - Información del proyecto
    """
    return Response({
        "autor": ["Alvaro Elo [ALZOR]"],
        "area": "Programación Back End",
        "proyecto": "ApiRest SmartConnect",
        "descripcion": "API RESTful desarrollada de forma autónoma con Django REST Framework, implementando autenticación segura mediante JWT",
        "version": "1.0"
    })


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar usuarios
    Admin: CRUD completo
    Operador: Solo lectura
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAdminOrReadOnly]


class DepartamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar departamentos
    Admin: CRUD completo
    Operador: Solo lectura
    """
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [IsAdminOrReadOnly]


class SensorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar sensores RFID
    Admin: CRUD completo
    Operador: Solo lectura
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def activar(self, request, pk=None):
        """Activa un sensor"""
        sensor = self.get_object()
        sensor.estado = Sensor.Estado.ACTIVO
        sensor.save()
        return Response({'status': 'sensor activado', 'sensor': SensorSerializer(sensor).data})

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def desactivar(self, request, pk=None):
        """Desactiva un sensor"""
        sensor = self.get_object()
        sensor.estado = Sensor.Estado.INACTIVO
        sensor.save()
        return Response({'status': 'sensor desactivado', 'sensor': SensorSerializer(sensor).data})

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def verificar_acceso(self, request):
        """
        Verifica si un sensor puede acceder
        Simula el flujo de validación de acceso
        """
        uid_mac = request.data.get('uid_mac')
        barrera_id = request.data.get('barrera_id')

        if not uid_mac:
            return Response(
                {'error': 'uid_mac es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            sensor = Sensor.objects.get(uid_mac=uid_mac)
        except Sensor.DoesNotExist:
            # Registrar evento de acceso denegado
            Evento.objects.create(
                tipo=Evento.TipoEvento.ACCESO_DENEGADO,
                motivo_denegacion='Sensor no encontrado',
                descripcion=f'Intento de acceso con UID/MAC: {uid_mac}'
            )
            return Response({
                'acceso': 'denegado',
                'motivo': 'Sensor no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)

        # Verificar estado del sensor
        if not sensor.esta_activo():
            motivo = f'Sensor en estado: {sensor.get_estado_display()}'
            Evento.objects.create(
                tipo=Evento.TipoEvento.ACCESO_DENEGADO,
                sensor=sensor,
                motivo_denegacion=motivo,
                descripcion=f'Sensor {sensor.nombre} intentó acceder'
            )
            return Response({
                'acceso': 'denegado',
                'motivo': motivo,
                'sensor': SensorSerializer(sensor).data
            }, status=status.HTTP_403_FORBIDDEN)

        # Acceso permitido
        evento_data = {
            'tipo': Evento.TipoEvento.ACCESO_PERMITIDO,
            'sensor': sensor,
            'descripcion': f'Acceso permitido para sensor {sensor.nombre}'
        }

        if barrera_id:
            try:
                barrera = Barrera.objects.get(id=barrera_id)
                evento_data['barrera'] = barrera
            except Barrera.DoesNotExist:
                pass

        Evento.objects.create(**evento_data)

        return Response({
            'acceso': 'permitido',
            'sensor': SensorSerializer(sensor).data,
            'mensaje': 'Acceso concedido'
        }, status=status.HTTP_200_OK)


class BarreraViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar barreras
    Admin: CRUD completo
    Operador: Solo lectura
    """
    queryset = Barrera.objects.all()
    serializer_class = BarreraSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def abrir(self, request, pk=None):
        """Abre la barrera manualmente"""
        barrera = self.get_object()
        barrera.abrir()
        
        # Registrar evento
        Evento.objects.create(
            tipo=Evento.TipoEvento.APERTURA_MANUAL,
            barrera=barrera,
            usuario_responsable=request.user,
            descripcion=f'Apertura manual de barrera {barrera.nombre} por {request.user.username}'
        )
        
        return Response({
            'status': 'barrera abierta',
            'barrera': BarreraSerializer(barrera).data
        })

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cerrar(self, request, pk=None):
        """Cierra la barrera manualmente"""
        barrera = self.get_object()
        barrera.cerrar()
        
        # Registrar evento
        Evento.objects.create(
            tipo=Evento.TipoEvento.CIERRE_MANUAL,
            barrera=barrera,
            usuario_responsable=request.user,
            descripcion=f'Cierre manual de barrera {barrera.nombre} por {request.user.username}'
        )
        
        return Response({
            'status': 'barrera cerrada',
            'barrera': BarreraSerializer(barrera).data
        })


class EventoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para consultar eventos (solo lectura)
    Todos los usuarios autenticados pueden ver eventos
    """
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]
