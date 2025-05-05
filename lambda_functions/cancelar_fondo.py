from app.controllers.FondosController import FondosController
from utils.exceptions import SuscripcionNoEncontradaError
import json


def cancelarFondo(event, context):
    try:
        body = json.loads(event['body']) if isinstance(event.get('body'), str) else event.get('body', {})
        
         # Validar campos requeridos
        required_fields = ['idFondo','idUsuario']
        if not all(field in body for field in required_fields):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Faltan campos: idFondo, idUsuario'})
            }
        
        controller = FondosController()
        response = controller.cancelar_suscripcion(
            id_fondo=body['idFondo'],
            id_usuario=body['idUsuario']
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(response, default=str)
        }
    except SuscripcionNoEncontradaError:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'No existe una suscripción activa para este fondo'})
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error interno'})
        }