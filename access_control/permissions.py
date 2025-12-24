from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado:
    - Admin: puede hacer todo (CRUD completo)
    - Operador: solo puede leer (GET)
    """
    def has_permission(self, request, view):
        # Permitir lectura a todos los usuarios autenticados
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Permitir escritura solo a administradores
        return request.user and request.user.is_authenticated and request.user.es_admin()


class IsAdmin(permissions.BasePermission):
    """
    Permiso que solo permite acceso a administradores
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.es_admin()
