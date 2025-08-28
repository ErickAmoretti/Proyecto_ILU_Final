from Models.roles_model import Roles
from flask import jsonify, request
from Schemas.roles_schema import Roles_schema, Rol_schema
from config import db
# from flask_jwt_extended import create_access_token, jwt_required - Pendiente


def get_roles():
    try: 
        roles = Roles.query.all()
        return jsonify(Roles_schema.dump(roles))
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
    
def create_rol():
    try: 
        data = request.get_json()
        if not data:
            return jsonify({"message": "Error: No data received"}), 400

        validate_data = Rol_schema.load(data)
        rol = Roles(**validate_data)
        db.session.add(rol)
        db.session.commit()

        return jsonify({"status": "Success", "data": Rol_schema.dump(rol)}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {str(e)}"}), 500
    
def update_rol(id):
    try:
        rol = Roles.query.get(id)
        data = request.get_json()
        if not data: 
            return jsonify({"message": "Error: No data received"}), 400
        
        validate_data = Rol_schema.load(data, partial=True)
        for key, value in validate_data.items():
            setattr(rol, key, value)

        db.session.commit()
        return jsonify({"status": "Success", "data": Rol_schema.dump(rol)}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {str(e)}"}), 500
    
def delete_rol(id):
    try:
        rol = Roles.query.get(id)
        db.session.delete(rol)
        db.session.commit()
        return jsonify({"status": "Success", "message": f"Task with id {id} deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"error: {str(e)}"}), 500