# lambda_functions/historial.py
from app.controllers.TransaccionesController import TransaccionesController
from utils.exceptions import UsuarioNoEncontradoError
import json

def obtener_historial(event, context):
   try:
        id_usuario = event['pathParameters']['idUsuario']
        controller = TransaccionesController()
        historial = controller.obtener_historial(id_usuario)
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(historial, default=str)
        }
   except UsuarioNoEncontradoError:
       
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Usuario no encontrado'})
        }
   except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error al obtener historial'})
        }