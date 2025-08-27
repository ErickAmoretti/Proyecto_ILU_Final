from flask import Flask 
from flask_jwt_extended import JWTManager
from config import conf_database
from routes import tarea_bp, usuario_bp, proyecto_bp


app = Flask(__name__)
jwt = JWTManager(app)

conf_database(app)

app.register_blueprint(proyecto_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(tarea_bp)


if __name__ == '__main__':
    app.run(debug=True)