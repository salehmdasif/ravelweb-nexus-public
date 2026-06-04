"""
Tenant provisioning: create organizations, databases, and run schema migrations.

When a user activates a license key, this module:
  1. Creates a new PostgreSQL database for the tenant.
  2. Applies all tenant schema migrations to the new database.
  3. Registers the organization and database mapping in the main database.

If any step after database creation fails, the physical database is dropped
and the main database transaction is rolled back to prevent orphaned resources.
"""


def generate_db_name(org_name: str) -> str:
    """
    Generate a unique, safe PostgreSQL database name from an organization name.

    Args:
        org_name: The organization/shop name as entered by the user.

    Returns:
        str: A sanitized database name, e.g. 'tenant_myshop_1748901234'.

    Note:
        Generation algorithm is proprietary and not included in this public version.
    """
    raise NotImplementedError("Proprietary implementation")


def provision_tenant(org_name: str, main_conn) -> tuple[int, str]:
    """
    Atomically create a new organization and its tenant database.

    Steps:
        1. Create a new PostgreSQL database (autocommit, cannot be rolled back).
        2. Apply all tenant schema migrations to the new database.
        3. Insert organization and tenant_database records in the main database.

    If step 2 or 3 fails, the physical database is dropped and main_conn is
    rolled back to leave no orphaned resources.

    Args:
        org_name: The organization/shop name.
        main_conn: Open psycopg2 connection to the main database.

    Returns:
        tuple[int, str]: (organization_id, db_name)

    Raises:
        Exception: If any provisioning step fails after database creation.

    Note:
        Core provisioning logic is proprietary and not included in this public version.
    """
    raise NotImplementedError("Proprietary implementation")


def sync_user_to_main(user_data: dict, main_conn):
    """
    Insert or update a user record in the main/control database.

    Uses INSERT ... ON CONFLICT DO UPDATE to handle both new users and updates.

    Args:
        user_data: Dict with user field values (id, name, email, role_id, etc.).
        main_conn: Open psycopg2 connection to the main database.

    Note:
        Implementation is proprietary and not included in this public version.
    """
    raise NotImplementedError("Proprietary implementation")


def sync_user_to_tenant(user_data: dict, tenant_conn):
    """
    Insert or update a user record in a tenant database.

    The tenant database mirrors the main database's users table for JOIN queries.
    Role name resolution is handled automatically.

    Args:
        user_data: Dict with user field values.
        tenant_conn: Open psycopg2 connection to the tenant database.

    Note:
        Implementation is proprietary and not included in this public version.
    """
    raise NotImplementedError("Proprietary implementation")


def get_tenant_db_name(org_id: int, main_conn) -> str | None:
    """
    Look up the tenant database name for an organization.

    Args:
        org_id: Organization primary key.
        main_conn: Open psycopg2 connection to the main database.

    Returns:
        str | None: The database name, or None if not found.
    """
    raise NotImplementedError("Proprietary implementation")
