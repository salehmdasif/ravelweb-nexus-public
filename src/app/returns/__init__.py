from flask import Blueprint

bp = Blueprint('returns', __name__, url_prefix='/returns')

from . import routes  # noqa: F401, E402
