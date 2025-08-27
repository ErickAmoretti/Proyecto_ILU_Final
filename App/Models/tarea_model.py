from config import db 
from sqlalchemy.dialects.mysql import TINYINT

class Tarea(db.Model):
    __tablename__ = "Tareas"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nombre = db.Column(db.String(70), unique = True, nullable = False)
    descripcion = db.Column(db.String(255), nullable = True)
    estatus = db.Column(TINYINT, default = 0)
    id_proyecto = db.Column(db.Integer, db.ForeignKey('Proyectos.id'), nullable = False)

    def __init__(self, nombre, descripcion, estatus, id_proyecto):
        self.nombre = nombre
        self.descripcion = descripcion
        self.estatus = estatus
        self.id_proyecto = id_proyecto