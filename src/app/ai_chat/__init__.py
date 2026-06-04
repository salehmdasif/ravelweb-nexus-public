from flask import Blueprint

bp = Blueprint('ai_chat', __name__, url_prefix='/ai-chat')

from . import routes  # noqa: F401, E402
