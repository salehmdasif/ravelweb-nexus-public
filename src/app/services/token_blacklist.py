"""
Token and session revocation via Redis.

Provides functions for:
  - Revoking individual user sessions (e.g. on deactivation).
  - Revoking all sessions for a tenant (e.g. on license suspension).
  - Checking revocation status on every request.

Redis keys use a TTL matched to the maximum session lifetime so the store
self-cleans without any maintenance jobs.
"""


def revoke_user(user_id: int):
    """
    Signal that all sessions for this user should be terminated.

    Args:
        user_id: The user whose sessions should be invalidated.

    Note:
        Revocation signal format and TTL strategy are proprietary and not
        included in this public version.
    """
    raise NotImplementedError("Proprietary implementation")


def revoke_tenant(org_id: int):
    """
    Signal that all sessions for this tenant/organization should be terminated.

    Args:
        org_id: The organization whose tenant sessions should be invalidated.

    Note:
        Implementation is proprietary and not included in this public version.
    """
    raise NotImplementedError("Proprietary implementation")


def is_user_revoked(user_id: int, login_time: float) -> bool:
    """
    Check whether this user's session was revoked after they logged in.

    Args:
        user_id: The user to check.
        login_time: Unix timestamp from session['login_time'].

    Returns:
        bool: True if the session should be terminated.

    Note:
        Check logic is proprietary and not included in this public version.
    """
    raise NotImplementedError("Proprietary implementation")


def is_tenant_revoked(org_id: int, login_time: float) -> bool:
    """
    Check whether this tenant's sessions were revoked after the user logged in.

    Args:
        org_id: The organization to check.
        login_time: Unix timestamp from session['login_time'].

    Returns:
        bool: True if the session should be terminated.

    Note:
        Check logic is proprietary and not included in this public version.
    """
    raise NotImplementedError("Proprietary implementation")
