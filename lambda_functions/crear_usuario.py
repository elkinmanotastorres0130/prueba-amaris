from app.controllers.UsuariosController import UsuariosController
import json
from utils.exceptions import CustomAppError
import traceback

def crear_usuario(event, context):
    try:
         # Parsear el body (viene como string desde API Gateway)
        body = json.loads(event['body']) if isinstance(event.get('body'), str) else event.get('body', {})
        
        # Validar campos requeridos
        required_fields = ['nombre','correo', 'edad','identificacion', 'monto']
        if not all(field in body for field in required_fields):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Faltan campos: nombre, edad, monto'})
            }

        controller = UsuariosController()
        id_usuario = controller.crear_usuario(
            nombre=body.get('nombre'),
            correo=body.get('correo'),
            edad=body.get('edad'),
            identificacion=body.get('identificacion'),
            monto=body.get('monto')
        )
        return {
            'statusCode': 201,
           
            'body': json.dumps({
                'idUsuario': id_usuario,
                'message': 'Usuario creado'
            })
        }
    except CustomAppError as ce:
        print("⚠️ Error de negocio:", ce.message)
        return {
            'statusCode': ce.status_code,
            'body': json.dumps({'error': ce.message})
        }

    except Exception as e:
        print("❌ Error inesperado:")
        print(f"ERROR: {str(e)}")  # Log en CloudWatch
        traceback.print_exc()
        return {
            'statusCode': 500,
          
            'body': json.dumps({'error': 'Error interno'})
        }