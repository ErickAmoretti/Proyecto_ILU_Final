from Models.tarea_model import Tarea
from flask import jsonify, request
from Schemas.tarea_schema import Tarea_schema, Tareas_schema
from config import db
from flask_jwt_extended import get_jwt, jwt_required

@jwt_required()
def get_tarea(id):
    try:
        claims = get_jwt()
        if claims.get('role') not in ['normal', 'admin']:
            return jsonify({"message": "Role required"}), 403
        
        tarea = Tarea.query.get(id)
        if tarea:
            return jsonify(Tarea_schema.dump(tarea))

        return jsonify({"message": "Task not found"}), 404

    except Exception as e: 
        return jsonify({"message": f"Error: {str(e)}"}), 500
    
@jwt_required()
def get_tareas():
    try: 

        claims = get_jwt()
        if claims.get('role') not in ['normal', 'admin']:
            return jsonify({"message": "Role required"}), 403
        
        tareas = Tarea.query.all()
        return jsonify(Tareas_schema.dump(tareas))
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@jwt_required()
def create_tarea():
    try: 
        claims = get_jwt()
        if claims.get('role') not in ['normal', 'admin']:
            return jsonify({"message": "Role required"}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({"message": "Error: No data received"}), 400

        validate_data = Tarea_schema.load(data)
        tarea = Tarea(**validate_data)
        db.session.add(tarea)
        db.session.commit()

        return jsonify({"status": "Success", "data": Tarea_schema.dump(tarea)}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {str(e)}"}), 500

@jwt_required()
def update_tarea(id):
    try:

        claims = get_jwt()
        if claims.get('role') not in ['normal', 'admin']:
            return jsonify({"message": "Role required"}), 403
        
        tarea = Tarea.query.get(id)
        data = request.get_json()
        if not data: 
            return jsonify({"message": "Error: No data received"}), 400
        
        validate_data = Tarea_schema.load(data, partial=True)
        for key, value in validate_data.items():
            setattr(tarea, key, value)

        db.session.commit()
        return jsonify({"status": "Success", "data": Tarea_schema.dump(tarea)}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {str(e)}"}), 500

@jwt_required()
def delete_tarea(id):
    try:
        claims = get_jwt()
        if claims.get('role') not in ['normal', 'admin']:
            return jsonify({"message": "Role required"}), 403
        
        tarea = Tarea.query.get(id)
        db.session.delete(tarea)
        db.session.commit()
        return jsonify({"status": "Success", "message": f"Task with id {id} deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"error: {str(e)}"}), 500