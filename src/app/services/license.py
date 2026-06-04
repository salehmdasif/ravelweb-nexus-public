"""
SaaS license service: key generation, validation, and activation.

This module handles the full license lifecycle:
  - Generating unique license keys for approved shop requests.
  - Validating a key's status, expiry, and binding before activation.
  - Activating a key by provisioning a tenant database and binding the license.
"""

from app.db import get_main_db


def generate_license_key(shop_name: str) -> str:
    """
    Generate a unique license key for a shop.

    Args:
        shop_name: The business name for which the key is generated.

    Returns:
        str: A unique license key string.

    Note:
        Key generation algorithm is proprietary and not included in this public version.
    """
    raise NotImplementedError("Proprietary implementation")


def validate_license(license_key: str, requesting_user_id: int = None) -> dict:
    """
    Validate a SaaS license key before activation.

    Checks:
        - Key exists in the database.
        - Key is not revoked or inactive.
        - Key is not expired.
        - Key is not already bound to another user (if bound).

    Args:
        license_key: The license key string to validate.
        requesting_user_id: Optional user ID for binding checks.

    Returns:
        dict with keys:
            valid (bool): True if the key can be activated.
            status (str): ok | not_found | revoked | inactive | expired | already_used | bound | already_active.
            license (dict | None): The license database record.
            error (str | None): Human-readable error message if not valid.

    Note:
        Validation logic is proprietary and not included in this public version.
    """
    raise NotImplementedError("Proprietary implementation")


def activate_license(license_key: str, user_id: int, main_conn) -> tuple[int, str]:
    """
    Activate a license: provision tenant and bind license to user.

    Args:
        license_key: The license key string to activate.
        user_id: The user activating the license.
        main_conn: Open psycopg2 connection to the main database.

    Returns:
        tuple[int, str]: (org_id, db_name) for the provisioned tenant.

    Raises:
        ValueError: If the license is invalid or unusable.
        RuntimeError: If provisioning fails.

    Note:
        Activation logic is proprietary and not included in this public version.
    """
    raise NotImplementedError("Proprietary implementation")
