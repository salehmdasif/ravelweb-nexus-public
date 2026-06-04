"""
Audit logging service.

Provides two audit functions:
  - log_action: writes to the tenant database audit_log table.
  - log_saas_event: writes to the main database admin_audit_log table.
"""

from flask import session, request


def log_action(action: str, module: str, record_id: int = None, description: str = None):
    """
    Write an audit entry to the current tenant's audit_log table.

    Args:
        action: Short action identifier (e.g. 'create', 'update', 'delete', 'void').
        module: Module name (e.g. 'sales', 'products', 'employees').
        record_id: Optional primary key of the affected record.
        description: Optional human-readable description of the action.

    Note:
        Implementation reads user context from the Flask session and IP from
        the request. Errors are silently suppressed so audit failures never
        break the main operation.
    """
    raise NotImplementedError("Proprietary implementation")


def log_saas_event(actor_id: int, action: str, target: str,
                   tenant_id: int = None, metadata: dict = None):
    """
    Write an audit entry to the main database admin_audit_log table.

    Used for platform-level events: tenant provisioning, license management,
    admin panel actions.

    Args:
        actor_id: ID of the superadmin performing the action.
        action: Dot-separated action identifier (e.g. 'tenant.provisioned').
        target: Description of what was acted on (e.g. 'org:42').
        tenant_id: Optional organization ID involved.
        metadata: Optional dict of additional context (stored as JSON).

    Note:
        Implementation is proprietary and not included in this public version.
    """
    raise NotImplementedError("Proprietary implementation")
