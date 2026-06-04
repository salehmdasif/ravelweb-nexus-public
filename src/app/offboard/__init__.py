from flask import Blueprint

bp = Blueprint('offboard', __name__, url_prefix='/offboard')

from . import routes  # noqa: F401, E402
