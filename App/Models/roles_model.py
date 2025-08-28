from config import db 

class Roles(db.Model):
    __tablename__ = "Roles"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    rol_nombre = db.Column(db.String(50), nullable = False)
    descripcion = db.Column(db.String(255), nullable = True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable = False)

    def __init__(self, rol_nombre, descripcion, id_usuario):
        self.rol_nombre = rol_nombre
        self.descripcion = descripcion
        self.id_usuario = id_usuario