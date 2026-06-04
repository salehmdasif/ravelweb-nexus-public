"""
Tenant middleware: resolves the correct tenant database before every request.

Registered as a Flask before_request hook. Sets g.org_id and g.db_name for
all authenticated requests. Enforces the pending-user redirect flow for users
who have registered but not yet activated a license.
"""

from flask import session, g, request, redirect, url_for, jsonify, flash


def init_tenant_middleware(app):
    """
    Register the tenant injection and enforcement hook on the Flask app.

    Args:
        app: Flask application instance.

    Note:
        Route allow-lists, session revocation checks, and enforcement logic
        are proprietary and not included in this public version.
    """
    @app.before_request
    def inject_and_enforce_tenant():
        """
        Resolve tenant context for the current request.

        Sets g.org_id and g.db_name from the session. Redirects unauthenticated
        users, pending users (no tenant), and revoked sessions.

        Note:
            Core logic is proprietary and not included in this public version.
        """
        raise NotImplementedError("Proprietary implementation")
