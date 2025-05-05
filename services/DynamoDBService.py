import boto3

class DynamoDBService:
    def __init__(self):
        self.resource = boto3.resource('dynamodb')

    def get_table(self, table_name):
        return self.resource.Table(table_name)