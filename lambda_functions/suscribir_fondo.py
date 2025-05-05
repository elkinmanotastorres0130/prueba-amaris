from app.controllers.FondosController import FondosController
from utils.exceptions import SaldoInsuficienteError, FondoNoEncontradoError, UsuarioNoEncontradoError
import json

def suscribir_fondo(event, context):
    try:
        body = json.loads(event['body']) if isinstance(event.get('body'), str) else event.get('body', {})
        
        required_fields = ['idFondo', 'idUsuario', 'montoApertura']
        if not all(field in body for field in required_fields):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Faltan campos: idFondo, idUsuario, montoApertura'})
            }
        
        controller = FondosController()
        response = controller.suscribir(
            id_fondo=body['idFondo'],
            id_usuario=body['idUsuario'],
            monto_apertura=body['montoApertura']
        )
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    except SaldoInsuficienteError as e:
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
    except (FondoNoEncontradoError, UsuarioNoEncontradoError) as e:
        print(e)
        return {
            'statusCode': 404,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error interno'})
        }