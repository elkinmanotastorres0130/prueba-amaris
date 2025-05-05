from app.controllers.FondosController import FondosController
from utils.exceptions import SuscripcionNoEncontradaError
from utils.response import generar_respuesta
import json

def cancelarFondo(event, context):
    """
    Función Lambda para cancelar una suscripción a un fondo.

    Parámetros:
    - event: Diccionario que contiene los datos de la solicitud HTTP. 
             Se espera que tenga un campo 'body' con un JSON que incluya 'idFondo' y 'idUsuario'.
    - context: Información del contexto de ejecución de AWS Lambda (no se utiliza en esta función).

    Retorna:
    - Un diccionario con los siguientes campos:
        - statusCode: Código HTTP que indica el resultado de la operación (200, 400, 404, 500).
        - body: Respuesta en formato JSON con el resultado o el mensaje de error.
    """
    try:
        # Parsear el cuerpo de la solicitud (event['body']) si es una cadena JSON
        body = json.loads(event['body']) if isinstance(event.get('body'), str) else event.get('body', {})
        
        # Verificar que el cuerpo contenga los campos requeridos
        required_fields = ['idFondo', 'idUsuario']
        if not all(field in body for field in required_fields):
           return generar_respuesta(400, {'error': 'Faltan campos: idFondo, idUsuario'})
        
        # Crear una instancia del controlador de fondos
        controller = FondosController()
        
        # Llamar al método cancelar_suscripcion del controlador con los datos proporcionados
        response = controller.cancelar_suscripcion(
            id_fondo=body['idFondo'],
            id_usuario=body['idUsuario']
        )
        
        # Retornar una respuesta exitosa con el resultado
        return generar_respuesta(200, response)
    except SuscripcionNoEncontradaError:
        # Manejar el caso en que no exista una suscripción activa para el fondo
          return generar_respuesta(404, {'error': 'No existe una suscripción activa para este fondo'})
    except Exception as e:
        # Manejar cualquier otro error inesperado
        print(e) 
        return generar_respuesta(500, {'error': 'Error interno'})