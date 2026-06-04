"""
Authentication middleware utilities.

Shared helpers for extracting and verifying auth context across request types
(web session and mobile API JWT).
"""


def get_current_user_id() -> int | None:
    """
    Return the authenticated user ID from the current request context.

    Checks Flask session for web requests. Returns None for unauthenticated requests.

    Returns:
        int | None: User ID, or None.

    Note:
        Implementation is proprietary and not included in this public version.
    """
    raise NotImplementedError("Proprietary implementation")
