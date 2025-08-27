from flask import request, jsonify
from Schemas.usuario_schema import Usuario_Schema, Usuarios_Schema
from Models.usuario_model import Usuario
from config import db
import bcrypt
from flask_jwt_extended import create_access_token # Aplicar luego de solucionar dudas , jwt_required


def get_usuario(id):
    try:
        usuario = Usuario.query.get(id)
        if usuario: 
            return jsonify(Usuario_Schema.dump(usuario))
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
    
def get_usuarios():
    try: 
        usuarios = Usuario.query.all()
        return jsonify(Usuarios_Schema.dump(usuarios))
    except Exception as e:
        jsonify({"message": f"Error: {str(e)}"})

def create_usuario():
    try:
        data = request.get_json()
        nombre = data['nombre']
        puesto = data['puesto']
        correo = data['correo']
        password = data['password']

        if Usuario.query.filter_by(correo = correo).first():
            return jsonify({"message": "Email already exists"})
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = Usuario(nombre = nombre, puesto = puesto, correo = correo, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {str(e)}"}), 500
    
def update_usuario(id):
    try: 
        usuario = Usuario.query.get(id)
        data = request.get_json()
        if not data: 
            return jsonify({"message": "Error, no data received"}), 400
        
        validate_data = Usuario_Schema.load(data, partial= True)
        for key, value in validate_data.items():
            setattr(usuario, key, value)

        db.session.commit()
        return jsonify({"status": "Success", "data": Usuario_Schema.dump(usuario)}), 200
    except Exception as e:
        db.session.rollback()
        jsonify({"message": f"Error: {str(e)}"}), 500

def delete_usuario(id):
    try:
        usuario = Usuario.query.get(id)
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({"status": "success", "message": f"User with id {id} deleted" }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {str(e)}"}), 500

def login():
    try:
        data = request.get_json()
        correo = data['correo']
        password = data['password']
        print('Received data', correo, password)

        user = Usuario.query.filter_by(correo=correo).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            access_token = create_access_token(identity=str(user.id))
            return jsonify({"message": "login success", "access_token": access_token})
        else: 
            return jsonify({"message": "login failed"}), 401
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500