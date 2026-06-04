from flask import Blueprint

bp = Blueprint('exports', __name__, url_prefix='/exports')

from . import routes  # noqa: F401, E402
