from app.controllers.UsuariosController import UsuariosController
from utils.exceptions import UsuarioNoEncontradoError
from utils.response import generar_respuesta

def listar_usuarios(event, context):
    """
    Función Lambda para listar usuarios o buscar un usuario específico por ID.

    Parámetros:
    - event: Diccionario que contiene los datos de la solicitud HTTP.
             Puede incluir 'pathParameters' con el 'idUsuario' para buscar un usuario específico.
    - context: Información del contexto de ejecución de AWS Lambda (no se utiliza en esta función).

    Retorna:
    - Un diccionario con los siguientes campos:
        - statusCode: Código HTTP que indica el resultado de la operación (200, 404, 500).
        - headers: Encabezados HTTP, incluyendo el tipo de contenido.
        - body: Respuesta en formato JSON con los datos del usuario(s) o el mensaje de error.
    """
    try:
        # Crear una instancia del controlador de usuarios
        controller = UsuariosController()
        
        # Caso 1: Filtrar por ID (si existe 'pathParameters' con 'idUsuario')
        if event.get('pathParameters') and 'idUsuario' in event['pathParameters']:
            id_usuario = event['pathParameters']['idUsuario']
            
            # Obtener los datos del usuario específico
            usuario = controller.obtener_usuario(id_usuario)
            
            # Retornar una respuesta exitosa con los datos del usuario
            return generar_respuesta(200, usuario)
        
        # Caso 2: Listar todos los usuarios
        else:
            # Obtener la lista de todos los usuarios
            usuarios = controller.listar_usuarios()
            
            # Retornar una respuesta exitosa con la lista de usuarios
            return generar_respuesta(200, usuarios)            
    except UsuarioNoEncontradoError:
        # Manejar el caso en que el usuario no exista
        return generar_respuesta(404, {'error': 'Usuario no encontrado'})
    except Exception as e:
        # Manejar cualquier otro error inesperado
        print(f"Error: {str(e)}") 
        return generar_respuesta(500, {'error': 'Error interno del servidor'})