from services.DynamoDBService import DynamoDBService
from datetime import datetime

class Cancelacion:
    def __init__(self):
        self.table = DynamoDBService().get_table('Cancelaciones')

    def crear(self, id_transaccion, id_usuario, monto):
        self.table.put_item(
            Item={
                'idTransaccion': id_transaccion,
                'idUsuario': id_usuario,
                'monto': monto,
                'fecha': datetime.now().isoformat(),
                'estado': 0  # 0 = Cancelado
            }
        )