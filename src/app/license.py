"""
JWT-based license verification for Ravelweb Nexus.

License keys are signed JWTs that encode client identity, product slug,
expiry date, and an optional shop name binding hash.

The verification process has two layers:
  1. JWT signature validation (proves the key was issued by this platform).
  2. Main database status check (catches revoked or suspended licenses instantly).
"""

import os


def decode_license(license_key: str) -> dict | None:
    """
    Decode and verify a JWT license key signature.

    Args:
        license_key: The raw JWT license key string.

    Returns:
        The decoded payload dict if the signature is valid, else None.

    Note:
        Verification algorithm and secret derivation are proprietary and not
        included in this public version.
    """
    raise NotImplementedError("Proprietary implementation")


def get_license_status(license_key: str, shop_name: str = None) -> dict:
    """
    Return the full status of a license key.

    Checks JWT signature validity, main database revocation status, shop name
    binding (if configured), and expiry date.

    Args:
        license_key: The raw JWT license key string.
        shop_name: Optional shop name for binding verification.

    Returns:
        dict with keys:
            valid (bool): True if the license is currently active.
            status (str): One of: missing, invalid, revoked, suspended, expired, active.
            expires_at (str | None): ISO date string of expiry, or None.
            days_remaining (int | None): Days until expiry, or None.
            client_name (str | None): Client identifier from the token.
            product_slug (str | None): Product identifier from the token.
            warning_level (str | None): One of: critical_3, warning_7, warning_14, or None.

    Note:
        Core validation logic is proprietary and not included in this public version.
    """
    raise NotImplementedError("Proprietary implementation")


def is_sales_allowed(license_key: str, shop_name: str = None) -> bool:
    """
    Return True if the license is valid and active.

    Args:
        license_key: The raw JWT license key string.
        shop_name: Optional shop name for binding verification.

    Returns:
        bool

    Note:
        Core logic is proprietary and not included in this public version.
    """
    raise NotImplementedError("Proprietary implementation")


def get_license_key_from_db() -> str:
    """
    Read the license key from the tenant database (shop_settings table).

    Falls back to the LICENSE_KEY environment variable if not found in the DB.

    Returns:
        str: The license key, or an empty string if not configured.
    """
    raise NotImplementedError("Proprietary implementation")


def get_shop_name_from_db() -> str:
    """
    Read the shop name from the tenant database (shop_settings table).

    Returns:
        str: The shop name, or an empty string if not configured.
    """
    raise NotImplementedError("Proprietary implementation")
