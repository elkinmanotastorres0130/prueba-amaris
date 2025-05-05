from app.controllers.FondosController import FondosController
from utils.exceptions import SaldoInsuficienteError, FondoNoEncontradoError, UsuarioNoEncontradoError
import json

def suscribir_fondo(event, context):
    """
    Función Lambda para suscribir a un usuario a un fondo de inversión.

    Parámetros:
    - event: Diccionario que contiene los datos de la solicitud HTTP.
             Se espera que tenga un campo 'body' con un JSON que incluya:
             'idFondo', 'idUsuario' y 'montoApertura'.
    - context: Información del contexto de ejecución de AWS Lambda (no se utiliza en esta función).

    Retorna:
    - Un diccionario con los siguientes campos:
        - statusCode: Código HTTP que indica el resultado de la operación (200, 400, 404, 500).
        - body: Respuesta en formato JSON con el resultado o el mensaje de error.
    """
    try:
        # Parsear el cuerpo de la solicitud (event['body']) si es una cadena JSON
        body = json.loads(event['body']) if isinstance(event.get('body'), str) else event.get('body', {})
        
        # Validar que los campos requeridos estén presentes en el cuerpo
        required_fields = ['idFondo', 'idUsuario', 'montoApertura']
        if not all(field in body for field in required_fields):
            return {
                'statusCode': 400,  
                'body': json.dumps({'error': 'Faltan campos: idFondo, idUsuario, montoApertura'})
            }
        
        # Crear una instancia del controlador de fondos
        controller = FondosController()
        
        # Llamar al método suscribir del controlador con los datos proporcionados
        response = controller.suscribir(
            id_fondo=body['idFondo'],
            id_usuario=body['idUsuario'],
            monto_apertura=body['montoApertura']
        )
        
        # Retornar una respuesta exitosa con el resultado de la suscripción
        return {
            'statusCode': 200, 
            'body': json.dumps(response)
        }
    except SaldoInsuficienteError as e:
        # Manejar el caso en que el usuario no tenga saldo suficiente
        print(e) 
        return {
            'statusCode': 400,  
            'body': json.dumps({'error': str(e)})
        }
    except (FondoNoEncontradoError, UsuarioNoEncontradoError) as e:
        # Manejar el caso en que el fondo o el usuario no existan
        print(e) 
        return {
            'statusCode': 404,  
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        # Manejar cualquier otro error inesperado
        print(e) 
        return {
            'statusCode': 500,  
            'body': json.dumps({'error': 'Error interno'})
        }