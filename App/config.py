from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def conf_database(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{DBMS}://{user}:{password}@{server}/{database}'.format(
        DBMS = 'mariadb+mariadbconnector',
        user= 'usrDev',
        password = 'pa%24%24word%2E%2D',
        server = 'mcu.calhasdfv17y.us-east-1.rds.amazonaws.com',
        database = 'dbSebas'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_strong_secret_key'
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    app.config['JWT_TOKEN_LOCATION'] = ['headers']


    db.init_app(app)
    """ with app.app_context():
        db.create_all() """