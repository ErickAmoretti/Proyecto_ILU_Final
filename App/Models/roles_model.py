from config import db 

class Roles(db.Model):
    __tablename__ = "Roles"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    rol_nombre = db.Column(db.String(50), unique = True, nullable = False)
    descripcion = db.Column(db.String(255), nullable = True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable = False)

    def __init__(self, nombre, rol_nombre, id_usuario):
        self.nombre = nombre
        self.rol_nombre = rol_nombre
        self.id_usuario = id_usuario