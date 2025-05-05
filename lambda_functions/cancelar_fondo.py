from app.controllers.FondosController import FondosController
from utils.exceptions import SuscripcionNoEncontradaError
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
            return {
                'statusCode': 400,  # Código HTTP 400: Solicitud incorrecta
                'body': json.dumps({'error': 'Faltan campos: idFondo, idUsuario'})
            }
        
        # Crear una instancia del controlador de fondos
        controller = FondosController()
        
        # Llamar al método cancelar_suscripcion del controlador con los datos proporcionados
        response = controller.cancelar_suscripcion(
            id_fondo=body['idFondo'],
            id_usuario=body['idUsuario']
        )
        
        # Retornar una respuesta exitosa con el resultado
        return {
            'statusCode': 200, 
            'body': json.dumps(response, default=str)
        }
    except SuscripcionNoEncontradaError:
        # Manejar el caso en que no exista una suscripción activa para el fondo
        return {
            'statusCode': 404, 
            'body': json.dumps({'error': 'No existe una suscripción activa para este fondo'})
        }
    except Exception as e:
        # Manejar cualquier otro error inesperado
        print(e) 
        return {
            'statusCode': 500, 
            'body': json.dumps({'error': 'Error interno'})
        }