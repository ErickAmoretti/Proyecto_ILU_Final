from config import db

class Usuario(db.Model):
    __tablename__ = "Usuarios"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nombre = db.Column(db.String(50), nullable = False)
    puesto = db.Column(db.String(50), nullable = False)
    correo = db.Column(db.String(80), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)

    def __init__(self, nombre, puesto, correo, password):
        self.nombre = nombre
        self.puesto = puesto
        self.correo = correo
        self.password = password