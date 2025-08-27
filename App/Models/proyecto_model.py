from config import db

class Proyecto(db.Model):
    __tablename__ = "Proyectos"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nombre = db.Column(db.String(70), unique = True, nullable = False)
    descripcion = db.Column(db.String(255), nullable = True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable = False)

def __init__(self, nombre, descripcion, id_usuario):
    self.nombre = nombre
    self.descripcion = descripcion
    self.id_usuario = id_usuario