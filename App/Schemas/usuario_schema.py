from marshmallow import Schema, fields

class UsuariosSchema(Schema):
    id = fields.Int()
    nombre = fields.Str(required=True)
    puesto = fields.Str(required=True)
    correo = fields.Str(required=True)
    password = fields.Str(required=True)

Usuario_Schema = UsuariosSchema()
Usuarios_Schema = UsuariosSchema(many=True)