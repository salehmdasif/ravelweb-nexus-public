from flask import Blueprint

bp = Blueprint('vouchers', __name__, url_prefix='/vouchers')

from . import routes  # noqa: F401, E402
