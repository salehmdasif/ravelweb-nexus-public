from flask import Blueprint

bp = Blueprint('production', __name__, url_prefix='/production')

from . import routes  # noqa: F401, E402
