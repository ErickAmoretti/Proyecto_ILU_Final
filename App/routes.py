from flask import Blueprint
from Resources.usuario_resource import create_usuario, delete_usuario, update_usuario, get_usuarios, get_usuario, login
from Resources.proyecto_resource import create_proyecto, get_proyecto, get_proyectos, update_proyecto, delete_proyecto
from Resources.tarea_resource import create_tarea, get_tarea, get_tareas, update_tarea, delete_tarea
from Resources.roles_resources import create_rol, delete_rol, get_roles, update_rol

usuario_bp = Blueprint('Usuarios', __name__)

usuario_bp.route('/auth/login', methods=['POST'])(login)
usuario_bp.route('/auth/register', methods=['POST'])(create_usuario)

usuario_bp.route('/users/', methods=['GET'])(get_usuarios)
usuario_bp.route('/users/<int:id>', methods=['GET'])(get_usuario)
usuario_bp.route('/users/<int:id>', methods=['PUT'])(update_usuario)
usuario_bp.route('/users/<int:id>', methods=['DELETE'])(delete_usuario)

proyecto_bp = Blueprint('Proyectos', __name__)

proyecto_bp.route('/projects', methods=['GET'])(get_proyectos)
proyecto_bp.route('/projects/<int:id>', methods=['GET'])(get_proyecto)
proyecto_bp.route('/projects', methods=['POST'])(create_proyecto)
proyecto_bp.route('/projects/<int:id>', methods=['PUT'])(update_proyecto)
proyecto_bp.route('/projects/<int:id>', methods=['DELETE'])(delete_proyecto)

tarea_bp = Blueprint('Tareas', __name__)

tarea_bp.route('/projects/task/<int:id>', methods=['GET'])(get_tarea)
tarea_bp.route('/projects/task', methods=['GET'])(get_tareas)
tarea_bp.route('/projects/task', methods=['POST'])(create_tarea)
tarea_bp.route('/projects/task/<int:id>', methods=['PUT'])(update_tarea)
tarea_bp.route('/projects/task/<int:id>', methods=['DELETE'])(delete_tarea)

roles_bp = Blueprint('Roles', __name__)

roles_bp.route('/roles', methods=["GET"])(get_roles)
roles_bp.route('/roles', methods=['POST'])(create_rol)
roles_bp.route('/roles/<int:id>', methods=['PUT'])(update_rol)
roles_bp.route('/roles/<int:id>', methods=['DELETE'])(delete_rol)

