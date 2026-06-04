from flask import Blueprint

bp = Blueprint('payment_methods', __name__, url_prefix='/payment-methods')

from . import routes  # noqa: F401, E402
