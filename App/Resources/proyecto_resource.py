from Models.proyecto_model import Proyecto
from flask import jsonify, request
from Schemas.proyecto_schema import proyecto_schema, proyectos_schema
from config import db
from flask_jwt_extended import jwt_required, get_jwt

@jwt_required()
def get_proyecto(id):
    try: 
        claims = get_jwt()
        if claims.get('role') not in ['normal', 'admin']:
            return jsonify({"message": "Role required"}), 403

        proyecto = Proyecto.query.get(id)
        if proyecto:
            return jsonify(proyecto_schema.dump(proyecto))
        
        return jsonify({"message": "Project not found"}), 404
    
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@jwt_required()    
def get_proyectos():
    try: 
        claims = get_jwt()
        if claims.get('role') not in ['admin']:
            return jsonify({"message": "Role required"}), 403
        proyectos = Proyecto.query.all()
        return jsonify(proyectos_schema.dump(proyectos))
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@jwt_required()
def create_proyecto():
    try: 
        claims = get_jwt()
        if claims.get('role') not in ['admin']:
            return jsonify({"message": "Role required"}), 403
        data = request.get_json()
        if not data: 
            return jsonify({"message": "Error: No tada received"}), 400
        
        validate_data = proyecto_schema.load(data)
        proyecto = Proyecto(**validate_data)
        db.session.add(proyecto)
        db.session.commit()

        return jsonify({"status": "Success", "data": proyecto_schema.dump(proyecto)}), 201
    
    except Exception as e: 
        db.session.rollback()
        return jsonify({"message": f"Error: {str(e)}"}), 500

@jwt_required()
def update_proyecto(id):
    try: 
        claims = get_jwt()
        if claims.get('role') not in ['admin']:
            return jsonify({"message": "Role required"}), 403
        
        proyecto = Proyecto.query.get(id)
        data = request.get_json()

        if not data:
            return jsonify({"message": "Error: No data received"}), 400
        
        validate_data = proyecto_schema.load(data, partial=True)
        for key, value in validate_data.items():
            setattr(proyecto, key, value)

        db.session.commit()
        return jsonify({"status": "Success", "data": proyecto_schema.dump(proyecto)}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {str(e)}"}), 500

@jwt_required()
def delete_proyecto(id):
    try: 
        claims = get_jwt()
        if claims.get('role') not in ['admin']:
            return jsonify({"message": "Role required"}), 403
        
        proyecto = Proyecto.query.get(id)
        db.session.delete(proyecto)
        db.session.commit()
        return jsonify({"status": "Success", "message": f"Project with id {id} deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {str(e)}"}), 500