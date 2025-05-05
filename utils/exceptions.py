class CustomAppError(Exception):
    """Excepción base para errores personalizados en la app."""
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class SaldoInsuficienteError(CustomAppError):
    """Excepción lanzada cuando un usuario no tiene saldo suficiente."""
    def __init__(self, mensaje=None, nombre_fondo=None):
        if mensaje:
            super().__init__(mensaje, status_code=400)
        elif nombre_fondo:
            super().__init__(f"No tiene saldo disponible para vincularse al fondo {nombre_fondo}", status_code=400)
        else:
            super().__init__("Saldo insuficiente", status_code=400)

class FondoNoEncontradoError(CustomAppError):
    """Excepción lanzada cuando el fondo no existe."""
    def __init__(self):
        super().__init__("Fondo no encontrado", status_code=404)

class UsuarioNoEncontradoError(CustomAppError):
    """Excepción lanzada cuando el usuario no existe."""
    def __init__(self):
        super().__init__("Usuario no encontrado", status_code=404)
        
class SuscripcionNoEncontradaError(CustomAppError):
    """Excepción lanzada cuando el usuario no existe."""
    def __init__(self):
        super().__init__("No se encontro una suscripcion a un fondo para ese usuario", status_code=404)

# Puedes agregar más excepciones heredando de CustomAppError
