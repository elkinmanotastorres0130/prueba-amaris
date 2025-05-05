from app.controllers.UsuariosController import UsuariosController
from utils.exceptions import UsuarioNoEncontradoError
import json

def listar_usuarios(event, context):
    try:
        controller = UsuariosController()
        
        # Caso 1: Filtrar por ID (si existe pathParameters)
        if event.get('pathParameters') and 'idUsuario' in event['pathParameters']:
            id_usuario = event['pathParameters']['idUsuario']
            usuario = controller.obtener_usuario(id_usuario)
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(usuario, default=str)
            }
        
        # Caso 2: Listar todos los usuarios
        else:
            usuarios = controller.listar_usuarios()
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(usuarios, default=str)
            }
            
    except UsuarioNoEncontradoError:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Usuario no encontrado'})
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error interno del servidor'})
        }