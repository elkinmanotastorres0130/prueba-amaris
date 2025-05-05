from services.DynamoDBService import DynamoDBService
from datetime import datetime

class Suscripcion:
    def __init__(self):
        self.table = DynamoDBService().get_table('Suscripciones')

    def crear(self, id_usuario, id_fondo, monto):
        suscripcion = {
            'idUsuario': id_usuario,
            'idFondo': id_fondo,
            'monto': monto,
            'fecha': datetime.now().isoformat(),
            'estado': 1
        }
        self.table.put_item(Item=suscripcion)
        
    def obtener_por_ids(self, id_usuario, id_fondo):
        response = self.table.get_item(
            Key={
                'idUsuario': id_usuario,
                'idFondo': id_fondo
            }
        )
        return response.get('Item')

    def actualizar_estado(self, id_usuario, id_fondo, estado):
        self.table.update_item(
            Key={
                'idUsuario': id_usuario,
                'idFondo': id_fondo
            },
            UpdateExpression='SET estado = :estado',
            ExpressionAttributeValues={':estado': estado}
        )