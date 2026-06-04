from flask import Blueprint

bp = Blueprint('quotations', __name__, url_prefix='/quotations')

from . import routes  # noqa: F401, E402
