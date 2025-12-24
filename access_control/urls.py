from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    api_info, UsuarioViewSet, DepartamentoViewSet,
    SensorViewSet, BarreraViewSet, EventoViewSet
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'departamentos', DepartamentoViewSet)
router.register(r'sensores', SensorViewSet)
router.register(r'barreras', BarreraViewSet)
router.register(r'eventos', EventoViewSet)

urlpatterns = [
    path('info/', api_info, name='api-info'),
    path('', include(router.urls)),
]
