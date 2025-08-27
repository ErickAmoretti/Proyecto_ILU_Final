from marshmallow import fields, Schema

class TareasSchema(Schema):
    id = fields.Int()
    nombre = fields.Str(required=True)
    descripcion = fields.Str(required=False)
    estatus = fields.Int(required=True)
    id_proyecto = fields.Int(required=True)

Tarea_schema = TareasSchema()
Tareas_schema = TareasSchema(many=True)