# app/controllers/TransaccionesController.py
from models.Transaccion import Transaccion
from models.Usuario import Usuario
from models.Fondo import Fondo
from utils.exceptions import FondoNoEncontradoError, SaldoInsuficienteError

class TransaccionesController:
    def __init__(self):
        self.transaccion_model = Transaccion()
        self.usuario_model = Usuario()
        self.fondo_model = Fondo()

    def cancelar_fondo(self, id_fondo, id_usuario="usuario_default"):
        fondo = self.fondo_model.get_by_id(id_fondo)
        if not fondo:
            raise FondoNoEncontradoError()

        usuario = self.usuario_model.get_by_id(id_usuario)
        monto_devolucion = fondo['montoMinimo']

        # Registrar transacción de cancelación
        self.transaccion_model.crear(
            id_usuario=id_usuario,
            id_fondo=id_fondo,
            tipo="cancelacion",
            monto=monto_devolucion
        )

        # Devolver saldo al usuario
        self.usuario_model.actualizar_saldo(id_usuario, monto_devolucion)

        return {"message": "Cancelación exitosa"}

    def obtener_historial(self, id_usuario):
        transacciones = self.transaccion_model.obtener_por_usuario(id_usuario)
        
        historial = []
        for transaccion in transacciones:
            
            # Obtener nombres (cachear si hay muchas transacciones)
            usuario = self.usuario_model.obtener_por_id(transaccion['idUsuario'])
            fondo = self.fondo_model.obtener_por_id(transaccion['idFondo'])
            
            historial.append({
                'idTransaccion': transaccion['idTransaccion'],
                'tipo': transaccion['tipo'],
                'monto': float(transaccion['monto']),
                'fecha': transaccion['fecha'],
                'usuario': usuario.get('nombre', ''),
                'fondo': fondo.get('nombre', '')
            })
        
        return historial
