from Models.tarea_model import Tarea
from Models.proyecto_model import Proyecto
from flask import jsonify, request
from Schemas.tarea_schema import Tarea_schema, Tareas_schema
from config import db
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity

@jwt_required()
def get_tarea(id):
    try:
        claims = get_jwt()
        user_id = int(get_jwt_identity())
        tarea = Tarea.query.get(id)
        
        if not tarea:
            return jsonify({"message": "Task not found"}), 404
            
        # Los usuarios normales solo pueden acceder a las tareas de su proyecto
        if claims.get('role') == 'normal':
            proyecto = Proyecto.query.get(tarea.id_proyecto)
            if proyecto.id_usuario != user_id:
                return jsonify({"message": "Access denied"}), 403
                
        return jsonify(Tarea_schema.dump(tarea))

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
    
@jwt_required()
def get_tareas():
    try:
        claims = get_jwt()
        user_id = int(get_jwt_identity())
        
        if claims.get('role') == 'admin':
            tareas = Tarea.query.all()
        else: 
            # Se junta tarea con proyecto para poder hacer el query adecuado
            tareas = Tarea.query.join(Proyecto).filter(Proyecto.id_usuario == user_id).all()
            
        return jsonify(Tareas_schema.dump(tareas))
    
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@jwt_required()
def create_tarea():
    try:
        claims = get_jwt()
        if claims.get('role') not in ['normal', 'admin']:
            return jsonify({"message": "Valid role required"}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({"message": "Error: No data received"}), 400
        
        if claims.get('role') == 'normal':
            proyecto = Proyecto.query.get(data.get('id_proyecto'))
            if not proyecto or proyecto.id_usuario != int(get_jwt_identity()):
                return jsonify({"message": "Access denied to project"}), 403

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
        user_id = int(get_jwt_identity())
        tarea = Tarea.query.get(id)
        
        if not tarea:
            return jsonify({"message": "Task not found"}), 404
            
        # Los usuarios normales solamente pueden actualizar tareas de su proyecto
        if claims.get('role') == 'normal':
            proyecto = Proyecto.query.get(tarea.id_proyecto)
            if proyecto.id_usuario != user_id:
                return jsonify({"message": "Access denied"}), 403
        
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
        user_id = int(get_jwt_identity())
        tarea = Tarea.query.get(id)
        
        if not tarea:
            return jsonify({"message": "Task not found"}), 404
            
        # Los usuarios normales solo pueden borrar tareas de su proyecto
        if claims.get('role') == 'normal':
            proyecto = Proyecto.query.get(tarea.id_proyecto)
            if proyecto.id_usuario != user_id:
                return jsonify({"message": "Access denied"}), 403
        
        db.session.delete(tarea)
        db.session.commit()
        return jsonify({"status": "Success", "message": f"Task with id {id} deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {str(e)}"}), 500