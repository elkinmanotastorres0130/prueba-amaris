from app.controllers.UsuariosController import UsuariosController
import json
from utils.exceptions import CustomAppError
import traceback
from utils.response import generar_respuesta

def crear_usuario(event, context):
    """
    Función Lambda para crear un nuevo usuario.

    Parámetros:
    - event: Diccionario que contiene los datos de la solicitud HTTP.
             Se espera que tenga un campo 'body' con un JSON que incluya:
             'nombre', 'correo', 'edad', 'identificacion' y 'monto'.
    - context: Información del contexto de ejecución de AWS Lambda (no se utiliza en esta función).

    Retorna:
    - Un diccionario con los siguientes campos:
        - statusCode: Código HTTP que indica el resultado de la operación (201, 400, 500).
        - body: Respuesta en formato JSON con el resultado o el mensaje de error.
    """
    try:
        # Parsear el cuerpo de la solicitud (event['body']) si es una cadena JSON
        body = json.loads(event['body']) if isinstance(event.get('body'), str) else event.get('body', {})
        
        # Validar que los campos requeridos estén presentes en el cuerpo
        required_fields = ['nombre', 'correo', 'edad', 'identificacion', 'monto']
        if not all(field in body for field in required_fields):
            return generar_respuesta(400, {'error': 'Faltan campos: nombre, edad, monto'})

        # Crear una instancia del controlador de usuarios
        controller = UsuariosController()
        
        # Llamar al método crear_usuario del controlador con los datos proporcionados
        id_usuario = controller.crear_usuario(
            nombre=body.get('nombre'),
            correo=body.get('correo'),
            edad=body.get('edad'),
            identificacion=body.get('identificacion'),
            monto=body.get('monto')
        )
        
        # Retornar una respuesta exitosa con el ID del usuario creado
        return generar_respuesta(201, {
            'idUsuario': id_usuario,
            'message': 'Usuario creado'
        })
    except CustomAppError as ce:
        # Manejar errores personalizados de la aplicación
        print("Error de negocio:", ce.message)
        return generar_respuesta(ce.status_code, {'error': ce.message})
    except Exception as e:
        # Manejar cualquier otro error inesperado
        print(f"ERROR: {str(e)}") 
        traceback.print_exc()  
        return generar_respuesta(500, {'error': 'Error interno'})