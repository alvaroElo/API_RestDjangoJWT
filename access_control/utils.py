from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Manejador de excepciones personalizado para REST Framework
    """
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            'error': True,
            'status_code': response.status_code,
            'message': None,
            'details': response.data
        }

        # Mensajes personalizados según el código de estado
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            custom_response_data['message'] = 'Error de validación'
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            custom_response_data['message'] = 'No autenticado. Debe proporcionar credenciales válidas.'
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            custom_response_data['message'] = 'No tiene permisos para realizar esta acción.'
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            custom_response_data['message'] = 'Recurso no encontrado.'
        elif response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
            custom_response_data['message'] = 'Método no permitido.'
        else:
            custom_response_data['message'] = 'Error en la solicitud.'

        response.data = custom_response_data

    return response
