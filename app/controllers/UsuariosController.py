from models.Usuario import Usuario
from utils.exceptions import UsuarioNoEncontradoError 

class UsuariosController:
    def __init__(self):
        self.usuario_model = Usuario()

    def crear_usuario(self, nombre, correo,edad, identificacion , monto):
        return self.usuario_model.crear(nombre,correo, edad, identificacion, monto)
     
    def listar_usuarios(self):
        return self.usuario_model.listar_todos()

    def obtener_usuario(self, id_usuario):
        usuario = self.usuario_model.obtener_por_id(id_usuario)
        if not usuario:
            raise UsuarioNoEncontradoError()
        return usuario