from config import db
from flask import request, jsonify
from Schemas.usuario_schema import Usuario_Schema, Usuarios_Schema
from Models.usuario_model import Usuario
from Models.roles_model import Roles
import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

@jwt_required()
def get_usuario(id):
    try:
        claims = get_jwt()
        if claims.get('role') not in ['admin']:
            return jsonify({"message": "Admin access required"}), 403
        usuario = Usuario.query.get(id)
        if usuario:
            return jsonify(Usuario_Schema.dump(usuario))
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@jwt_required()
def get_usuarios():
    try:
        claims = get_jwt()
        if claims.get('role') not in ['admin']:
            return jsonify({"message": "Admin access required"}), 403
        usuarios = Usuario.query.all()
        return jsonify(Usuarios_Schema.dump(usuarios))
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

def create_usuario():
    try:
        data = request.get_json()
        nombre = data['nombre']
        puesto = data['puesto']
        correo = data['correo']
        password = data['password']
        role = data.get('role', 'normal')  # Default to 'normal'
        descripcion = data.get('descripcion', '')

        if Usuario.query.filter_by(correo=correo).first():
            return jsonify({"message": "Email already exists"}), 409

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = Usuario(nombre=nombre, puesto=puesto, correo=correo, password=hashed_password)
        db.session.add(new_user)
        db.session.flush()

        new_role = Roles(rol_nombre=role, descripcion=descripcion, id_usuario=new_user.id)
        db.session.add(new_role)
        db.session.commit()
        return jsonify({"message": "User created successfully", "role": role}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {str(e)}"}), 500

@jwt_required()
def update_usuario(id):
    try:
        claims = get_jwt()
        if claims.get('role') not in ['admin'] and int(get_jwt_identity()) != id:
            return jsonify({"message": "Access denied"}), 403
        usuario = Usuario.query.get(id)
        data = request.get_json()
        if not data:
            return jsonify({"message": "Error, no data received"}), 400

        validate_data = Usuario_Schema.load(data, partial=True)
        for key, value in validate_data.items():
            setattr(usuario, key, value)

        if 'role' in data and claims.get('role') == 'admin':
            role = Roles.query.filter_by(id_usuario=id).first()
            if role:
                role.rol_nombre = data['role']
                role.descripcion = data.get('descripcion', role.descripcion)
            else:
                new_role = Roles(rol_nombre=data['role'], descripcion=data.get('descripcion', ''), id_usuario=id)
                db.session.add(new_role)

        db.session.commit()
        return jsonify({"status": "Success", "data": Usuario_Schema.dump(usuario)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {str(e)}"}), 500

@jwt_required()
def delete_usuario(id):
    try:
        claims = get_jwt()
        if claims.get('role') not in ['admin']:
            return jsonify({"message": "Admin access required"}), 403
        usuario = Usuario.query.get(id)
        Roles.query.filter_by(id_usuario=id).delete()
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({"status": "success", "message": f"User with id {id} deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {str(e)}"}), 500

def login():
    try:
        data = request.get_json()
        correo = data['correo']
        password = data['password']

        user = Usuario.query.filter_by(correo=correo).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            role = Roles.query.filter_by(id_usuario=user.id).first()
            role_name = role.rol_nombre if role else 'normal'
            access_token = create_access_token(
                identity=str(user.id),
                additional_claims={'role': role_name}
            )
            return jsonify({"message": "login success", "access_token": access_token, "role": role_name})
        else:
            return jsonify({"message": "login failed"}), 401
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500