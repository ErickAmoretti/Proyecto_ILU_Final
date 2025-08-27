from marshmallow import fields, Schema

class ProyectosSchema(Schema):
    id = fields.Int()
    nombre = fields.Str(required=True)
    descripcion = fields.str(required=True)
    id_usuario = fields.Int(required=True)

proyecto_schema = ProyectosSchema()
proyectos_schema = ProyectosSchema(many=True)