from marshmallow import fields, Schema

class RolesSchema(Schema):
    id = fields.Int()
    rol_nombre = fields.Str(required=True)
    descripcion = fields.Str(required=False)
    id_usuario = fields.Int(required=True)

Rol_schema = RolesSchema()
Roles_schema = RolesSchema(many=True)