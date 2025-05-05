import boto3
from services.DynamoDBService import DynamoDBService
from services.DynamoDBService import DynamoDBService
from utils.exceptions import FondoNoEncontradoError
from decimal import Decimal

class Fondo:
    def __init__(self):
        self.table = DynamoDBService().get_table('Fondos')

    def obtener_por_id(self, id_fondo):
        try:
            # Asegurar que el ID sea string (DynamoDB es case-sensitive)
            #id_fondo = str(id_fondo).strip()
            
            response = self.table.get_item(
                Key={'id': id_fondo},
                ConsistentRead=True
            )
            
            if 'Item' not in response:
                raise FondoNoEncontradoError()
            
            item = response['Item']
            
            # Validar campos obligatorios
            required_fields = ['nombre', 'monto_minimo', 'categoria']
            if not all(field in item for field in required_fields):
                raise FondoNoEncontradoError("Fondo tiene campos incompletos")
            
            # Convertir tipos Decimal a Python nativo
            return {
                'id': item['id'],
                'nombre': item['nombre'],
                'monto_minimo':item['monto_minimo'],
                'categoria': item['categoria']
            }
            
        except boto3.exceptions.Boto3Error as e:
            print(f"Error de DynamoDB: {str(e)}")
            raise FondoNoEncontradoError()
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            raise