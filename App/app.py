from flask import Flask 
from flask_jwt_extended import JWTManager
from config import conf_database, db
from routes import tarea_bp, usuario_bp, proyecto_bp, roles_bp
from flask_migrate import Migrate


app = Flask(__name__)
jwt = JWTManager(app)

conf_database(app)

migrate = Migrate(app, db)


app.register_blueprint(proyecto_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(tarea_bp)
app.register_blueprint(roles_bp)


if __name__ == '__main__':
    app.run(debug=True)