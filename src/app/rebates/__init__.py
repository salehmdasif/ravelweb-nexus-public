from flask import Blueprint

bp = Blueprint('rebates', __name__, url_prefix='/rebates')

from . import routes  # noqa: F401, E402
