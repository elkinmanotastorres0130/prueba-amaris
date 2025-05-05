import uuid
from datetime import datetime
from services.DynamoDBService import DynamoDBService

class Transaccion:
    def __init__(self):
        self.table = DynamoDBService().get_table('Transacciones')

    def crear(self, id_usuario, id_fondo, tipo, monto):
        transaccion = {
            'idTransaccion': str(uuid.uuid4()),
            'idUsuario': id_usuario,
            'idFondo': id_fondo,
            'tipo': tipo,
            'monto': monto,
            'fecha': datetime.now().isoformat()
        }
        self.table.put_item(Item=transaccion)
        return transaccion['idTransaccion']
    
    def obtener_por_usuario(self, id_usuario):
        response = self.table.query(
            IndexName='UsuarioIndex',  # Usar el GSI definido en serverless.yml
            KeyConditionExpression='idUsuario = :idUsuario',
            ExpressionAttributeValues={':idUsuario': id_usuario}
        )
        return response.get('Items', [])