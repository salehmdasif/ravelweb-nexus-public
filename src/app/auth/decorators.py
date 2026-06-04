from functools import wraps
from flask import session, redirect, url_for, abort


def login_required(f):
    """Redirect unauthenticated or locked-out users to login."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login'))
        if session.get('locked'):
            return redirect(url_for('auth.lock'))
        return f(*args, **kwargs)
    return decorated


def role_required(*roles):
    """
    Restrict route access to users with one of the specified roles.

    Usage:
        @role_required('Admin', 'Manager')
        def my_route():
            ...

    Args:
        *roles: Role name strings that are permitted to access the route.
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not session.get('user_id'):
                return redirect(url_for('auth.login'))
            if session.get('locked'):
                return redirect(url_for('auth.lock'))
            if session.get('role') not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated
    return decorator


def tenant_required(f):
    """
    Require an active session with a resolved tenant database name.

    Use on routes that call get_db() / get_tenant_db().
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login'))
        if session.get('locked'):
            return redirect(url_for('auth.lock'))
        if not session.get('db_name'):
            return redirect(url_for('shop_request.submit'))
        return f(*args, **kwargs)
    return decorated


def superadmin_session_required(f):
    """Require active session with the is_superadmin flag. For SaaS admin routes."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login'))
        if session.get('locked'):
            return redirect(url_for('auth.lock'))
        if not session.get('is_superadmin'):
            abort(403)
        return f(*args, **kwargs)
    return decorated


def setup_required(f):
    """Redirect to /auth/setup if the user has not completed their profile."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login'))
        if session.get('locked'):
            return redirect(url_for('auth.lock'))
        # Profile completeness check is proprietary -- not included in this public version
        return f(*args, **kwargs)
    return decorated
