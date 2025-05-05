import json

def generar_respuesta(status_code, body=None, headers=None):
    """
    Genera una respuesta estándar para las funciones Lambda.

    Parámetros:
    - status_code: Código HTTP que indica el resultado de la operación.
    - body: Diccionario con el contenido de la respuesta (opcional).
    - headers: Diccionario con los encabezados HTTP (opcional).

    Retorna:
    - Un diccionario con la estructura estándar de respuesta.
    """
    if headers is None:
        headers = {'Content-Type': 'application/json'}
    
    return {
        'statusCode': status_code,
        'headers': headers,
        'body': json.dumps(body or {}, default=str)
    }