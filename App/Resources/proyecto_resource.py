from Models.proyecto_model import Proyecto
from flask import jsonify, request
from Schemas.proyecto_schema import proyecto_schema, proyectos_schema
from config import db
# from flask_jwt_extended import create_access_token, jwt_required - Pendiente

def get_proyecto(id):
    try: 
        proyecto = Proyecto.query.get(id)
        if proyecto:
            return jsonify(proyecto_schema(proyecto))
        
        return jsonify({"message": "Project not found"}), 404
    
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
    
def get_proyectos():
    try: 
        proyectos = Proyecto.query.all()
        return jsonify(proyecto_schema.dump(proyectos))
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
    
def create_proyecto():
    try: 
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
    
def update_proyecto(id):
    try: 
        proyecto = Proyecto.query.get(id)
        data = request.get_json

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
    
def delete_proyecto(id):
    try: 
        proyecto = Proyecto.query.get(id)
        db.session.delete(proyecto)
        db.session.commit()
        return jsonify({"status": "Success", "message": f"Project with id {id} deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {str(e)}"}), 500