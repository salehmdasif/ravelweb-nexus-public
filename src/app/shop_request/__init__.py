from flask import Blueprint

bp = Blueprint('shop_request', __name__, url_prefix='/shop-request')

from . import routes  # noqa: F401, E402
