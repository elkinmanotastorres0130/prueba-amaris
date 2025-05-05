# Fondos de Inversión - Proyecto con AWS Lambda + Python

Este proyecto permite a los usuarios suscribirse y cancelar su participación en fondos de inversión, usando AWS Lambda y Serverless Framework.

# Funcionalidades

- Crear usuario
- Suscribirse a un fondo
- Cancelar suscripción y reembolsar dinero
- Registro de transacciones en DynamoDB
- Notificaciones por correo SMTP

# Tecnologías

- Python 3.8
- AWS Lambda + API Gateway
- Serverless Framework
- SMTP
- DynamoDB

# Requisitos

- Cuenta en AWS
- Tener configuradas credenciales en tu máquina 
- Serverless Framework instalado (npm install -g serverless)

# Endpoints y pruebas ejemplos:

# Crear usuario

curl -X POST https://<API_ID>.execute-api.us-east-1.amazonaws.com/dev/usuario/crear_usuario \
  -H "Content-Type: application/json" \
  -d '{
        "nombre": "Juan",
        "correo": "juan@gmail.com",
        "monto": 200000
      }'

# Suscribirse a un fondo

curl -X POST https://<API_ID>.execute-api.us-east-1.amazonaws.com/dev/fondos/suscribir \
  -H "Content-Type: application/json" \
  -d '{
        "idFondo": "fondo123",
        "idUsuario": "usuario456",
        "montoApertura": 125000
      }'

# Cancelar suscripción

curl -X POST https://<API_ID>.execute-api.us-east-1.amazonaws.com/dev/fondos/cancelar \
  -H "Content-Type: application/json" \
  -d '{
        "idFondo": "fondo123",
        "idUsuario": "usuario456"
      }'

# Ver historial

curl https://<API_ID>.execute-api.us-east-1.amazonaws.com/dev/fondos/historial?idUsuario=usuario456

# Despliegue

```bash
sls deploy

