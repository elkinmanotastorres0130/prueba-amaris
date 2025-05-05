from models.Fondo import Fondo
from models.Transaccion import Transaccion
from models.Usuario import Usuario
from models.Suscripcion import Suscripcion
from models.Cancelacion import Cancelacion

from services.NotificacionService import NotificacionService
from utils.exceptions import SaldoInsuficienteError, FondoNoEncontradoError, UsuarioNoEncontradoError, SuscripcionNoEncontradaError

class FondosController:
    def __init__(self):
        self.usuario_model = Usuario()
        self.fondo_model = Fondo()
        self.transaccion_model = Transaccion()
        self.suscripcion_model = Suscripcion()
        self.cancelacion_model = Cancelacion()
        
    def suscribir(self, id_fondo, id_usuario, monto_apertura):
        # 1. Validar existencia de usuario y fondo
        usuario = self.usuario_model.obtener_por_id(id_usuario)
        fondo = self.fondo_model.obtener_por_id(id_fondo)

        if not usuario:
            raise UsuarioNoEncontradoError()
        if not fondo:
            raise FondoNoEncontradoError()

        # 2. Validar saldo suficiente
        if usuario['monto'] < monto_apertura:
            raise SaldoInsuficienteError(nombre_fondo=fondo['nombre'])

        if monto_apertura < fondo['monto_minimo']:
            raise SaldoInsuficienteError(mensaje=f"El monto mínimo para este fondo es {fondo['monto_minimo']}")

        # 3. Registrar transacción
        id_transaccion = self.transaccion_model.crear(
            id_usuario=id_usuario,
            id_fondo=id_fondo,
            tipo="apertura",
            monto=monto_apertura
        )

        # 4. Crear suscripción
        self.suscripcion_model.crear(
            id_usuario=id_usuario,
            id_fondo=id_fondo,
            monto=monto_apertura
        )

        # 5. Actualizar saldo del usuario
        self.usuario_model.actualizar_saldo(
            id_usuario=id_usuario,
            monto=-monto_apertura  # Restar el monto
        )
        
        # Recargar datos del usuario para obtener el nuevo saldo
        usuario_actualizado = self.usuario_model.obtener_por_id(id_usuario)

        # 6. Enviar notificación
        NotificacionService().enviar_email(
            destino=usuario['correo'],
            asunto=f"Bienvenido al fondo {fondo['nombre']}",
           contenido_html = f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; border-radius: 10px; background: #f9f9f9; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
                    <h1 style="color: #2c3e50;">🎉 ¡Gracias por suscribirte!</h1>
                    <p style="font-size: 16px; color: #333;">Has invertido <strong style="color: #27ae60;">${monto_apertura}</strong> en el fondo <strong>{fondo['nombre']}</strong>.</p>
                    <p style="font-size: 16px; color: #333;">💰 Saldo restante: <strong style="color: #2980b9;">${usuario_actualizado['monto']}</strong></p>
                    <hr style="margin-top: 30px; border: none; border-top: 1px solid #ccc;">
                    <p style="font-size: 14px; color: #888;">Este es un mensaje automático, por favor no responder.</p>
                </div>
                """
)

        return {
            'idTransaccion': id_transaccion,
            'mensaje': 'Suscripción exitosa'
        }
       
    def cancelar_suscripcion(self, id_fondo, id_usuario):
        # 1. Verificar suscripción activa
        suscripcion = self.suscripcion_model.obtener_por_ids(id_usuario, id_fondo)
        if not suscripcion or suscripcion.get('estado') == 0:
            raise SuscripcionNoEncontradaError()

        # 2. Registrar transacción de cancelación
        id_transaccion = self.transaccion_model.crear(
            id_usuario=id_usuario,
            id_fondo=id_fondo,
            tipo="cancelacion",
            monto=suscripcion['monto']
        )

        # 3. Registrar en tabla Cancelaciones
        self.cancelacion_model.crear(
            id_transaccion=id_transaccion,
            id_usuario=id_usuario,
            monto=suscripcion['monto']
        )

        # 4. Actualizar suscripción (estado a 0)
        self.suscripcion_model.actualizar_estado(id_usuario, id_fondo, 0)

        # 5. Devolver saldo al usuario
        self.usuario_model.actualizar_saldo(
            id_usuario=id_usuario,
            monto=suscripcion['monto']
        )
        
         # 6. Obtener datos para el correo
        fondo = self.fondo_model.obtener_por_id(id_fondo)
        usuario = self.usuario_model.obtener_por_id(id_usuario)

        # 7. Enviar notificación
        NotificacionService().enviar_email(
            destino=usuario['correo'],
            asunto=f"Cancelación de fondo {fondo['nombre']}",
           contenido_html = f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; border-radius: 10px; background: #fdfdfd; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
                    <h1 style="color: #c0392b;">❌ Cancelación de suscripción</h1>
                    <p style="font-size: 16px; color: #333;">El monto <strong style="color: #d35400;">${suscripcion['monto']}</strong> que tenías en el fondo <strong>{fondo['nombre']}</strong> ha sido depositado nuevamente en tu cuenta.</p>
                    <p style="font-size: 16px; color: #333;">💰 Saldo actual: <strong style="color: #2980b9;">${usuario['monto']}</strong></p>
                    <hr style="margin-top: 30px; border: none; border-top: 1px solid #ccc;">
                    <p style="font-size: 14px; color: #888;">Gracias por confiar en nosotros.</p>
                </div>
                """
        )

        return {
            'idTransaccion': id_transaccion,
            'monto_devuelto': suscripcion['monto']
        }