import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

class NotificacionService:
    def enviar_email(self, destino, asunto, contenido_html):
        try:
            # Configurar mensaje
            mensaje = MIMEMultipart()
            mensaje['From'] = os.getenv('EMAIL_FROM')
            mensaje['To'] = destino
            mensaje['Subject'] = asunto
            mensaje.attach(MIMEText(contenido_html, 'html'))

            # Conectar y enviar
            with smtplib.SMTP(os.getenv('SMTP_SERVER'), os.getenv('SMTP_PORT')) as servidor:
                servidor.starttls()  # Encriptación TLS
                servidor.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWORD'))
                servidor.send_message(mensaje)
            
            print("Email enviado con éxito")
            return True
        except Exception as e:
            print(f"Error enviando email: {str(e)}")
            return False