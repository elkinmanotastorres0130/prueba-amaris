# app/models/Usuario.py
from services.DynamoDBService import DynamoDBService
from utils.exceptions import UsuarioNoEncontradoError
from services.DynamoDBService import DynamoDBService
import uuid

class Usuario:
    def __init__(self):
        self.table = DynamoDBService().get_table('Usuarios')

    def get_by_id(self, id_usuario):
        response = self.table.get_item(Key={'idUsuario': id_usuario})
        if not response.get('Item'):
            raise UsuarioNoEncontradoError()
        return response['Item']

    def actualizar_saldo(self, id_usuario, monto):
        try:
            self.table.update_item(
                Key={'idUsuario': id_usuario},
                UpdateExpression='SET monto = monto + :monto',
                ExpressionAttributeValues={':monto': monto},
                ConditionExpression='attribute_exists(idUsuario)'
            )
        except self.table.meta.client.exceptions.ConditionalCheckFailedException:
            raise UsuarioNoEncontradoError()

    def crear(self, nombre,correo, edad,identificacion, monto, estado=1):
        id_usuario = str(uuid.uuid4())  
        self.table.put_item(
            Item={
                'idUsuario': id_usuario,
                'nombre': nombre,
                'correo': correo,
                'edad': int(edad),
                'identificacion': int(identificacion),
                'monto': int(monto),
                'estado': int(estado)
            }
        )
        return id_usuario
    
    def listar_todos(self):
        response = self.table.scan()
        return response.get('Items', [])

    def obtener_por_id(self, id_usuario):
        response = self.table.get_item(Key={'idUsuario': id_usuario})
        return response.get('Item')
    