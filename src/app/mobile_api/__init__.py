from flask import Blueprint

bp = Blueprint('mobile_api', __name__, url_prefix='/api/v1')

from . import auth, dashboard, sales, purchases, products  # noqa: F401, E402
from . import customers, suppliers, ledger, reports, profile  # noqa: F401, E402
