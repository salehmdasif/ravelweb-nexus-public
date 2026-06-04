import psycopg2
import psycopg2.extras
import psycopg2.pool
import psycopg2.extensions
from flask import g, current_app, session


_tenant_pools: dict = {}


def get_main_db():
    """
    Return a connection to the main/control database.

    The main database stores organizations, users, licenses, and tenant routing metadata.

    Returns:
        psycopg2 connection with RealDictCursor factory.

    Note:
        Connection is opened lazily and cached on Flask's request context (g).
    """
    if 'main_db' not in g:
        g.main_db = psycopg2.connect(
            current_app.config['MAIN_DATABASE_URL'],
            cursor_factory=psycopg2.extras.RealDictCursor,
        )
    return g.main_db


def get_tenant_db():
    """
    Return a pooled connection to the current session's tenant database.

    Reads the tenant database name from the Flask session. Connections are
    sanitized on checkout to roll back any open or aborted transactions left
    by a previous request on the same pooled connection.

    Returns:
        psycopg2 connection with RealDictCursor factory.

    Raises:
        RuntimeError: If no tenant database name is found in the session.

    Note:
        Connection pool management logic is proprietary and not included in
        this public version.
    """
    raise NotImplementedError("Proprietary implementation")


# Backward-compatible alias used by all business route handlers
get_db = get_tenant_db


def get_tenant_db_by_org(org_id: int):
    """
    Return a pooled connection to a tenant database by organization ID.

    Used by the SaaS admin panel to access any tenant's database.

    Args:
        org_id: The organization's primary key in the main database.

    Returns:
        psycopg2 connection.

    Note:
        Implementation is proprietary and not included in this public version.
    """
    raise NotImplementedError("Proprietary implementation")


def close_db(e=None):
    """
    Return all connections to their pools at end of request.

    Registered as Flask teardown_appcontext handler.
    """
    raise NotImplementedError("Proprietary implementation")


def init_app(app):
    """Register the database teardown handler with the Flask application."""
    app.teardown_appcontext(close_db)


def auto_expense(cur, category_name: str, title: str, amount: float,
                 ref_type: str, ref_id: int, expense_date, recorded_by: int):
    """
    Insert an auto-generated expense entry under a system cost category.

    Uses an upsert (ON CONFLICT DO UPDATE) keyed on (ref_type, ref_id) to
    prevent duplicate expense entries for the same source record.

    Args:
        cur: psycopg2 cursor on the tenant database.
        category_name: Name of the system cost category.
        title: Human-readable expense description.
        amount: Expense amount.
        ref_type: Source record type (e.g. 'salary_payment', 'supplier_payment').
        ref_id: Source record primary key.
        expense_date: Date of the expense.
        recorded_by: User ID who triggered the auto-entry.

    Note:
        Core logic is proprietary and not included in this public version.
    """
    raise NotImplementedError("Proprietary implementation")
