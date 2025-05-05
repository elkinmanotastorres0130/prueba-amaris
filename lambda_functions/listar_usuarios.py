from app.controllers.TransaccionesController import TransaccionesController
from utils.exceptions import UsuarioNoEncontradoError
import json

def obtener_historial(event, context):
    """
    Función Lambda para obtener el historial de transacciones de un usuario.

    Parámetros:
    - event: Diccionario que contiene los datos de la solicitud HTTP.
             Se espera que tenga un campo 'pathParameters' con el 'idUsuario'.
    - context: Información del contexto de ejecución de AWS Lambda (no se utiliza en esta función).

    Retorna:
    - Un diccionario con los siguientes campos:
        - statusCode: Código HTTP que indica el resultado de la operación (200, 404, 500).
        - headers: Encabezados HTTP, incluyendo el tipo de contenido.
        - body: Respuesta en formato JSON con el historial o el mensaje de error.
    """
    try:
        # Obtener el ID del usuario desde los parámetros de la ruta
        id_usuario = event['pathParameters']['idUsuario']
        
        # Crear una instancia del controlador de transacciones
        controller = TransaccionesController()
        
        # Llamar al método obtener_historial del controlador con el ID del usuario
        historial = controller.obtener_historial(id_usuario)
        
        # Retornar una respuesta exitosa con el historial de transacciones
        return {
            'statusCode': 200,  
            'headers': {'Content-Type': 'application/json'},  
            'body': json.dumps(historial, default=str) 
        }
    except UsuarioNoEncontradoError:
        # Manejar el caso en que el usuario no exista
        return {
            'statusCode': 404, 
            'body': json.dumps({'error': 'Usuario no encontrado'})
        }
    except Exception as e:
        # Manejar cualquier otro error inesperado
        print(e) 
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error al obtener historial'})
        }