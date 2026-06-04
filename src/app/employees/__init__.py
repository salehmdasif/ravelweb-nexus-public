from flask import Blueprint

bp = Blueprint('employees', __name__, url_prefix='/employees')

from . import routes  # noqa: F401, E402
