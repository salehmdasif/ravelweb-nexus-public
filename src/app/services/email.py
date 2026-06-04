"""
Email service: SMTP-based transactional email dispatch.

Sends email verification OTPs, password recovery codes, and 500 error alerts.
SMTP configuration is read from app.config (loaded from environment variables).
"""


def send_otp_email(to_email: str, otp: str, purpose: str = 'verification'):
    """
    Send a one-time password to the user's email address.

    Args:
        to_email: Recipient email address.
        otp: The one-time password code.
        purpose: Context label for the email subject ('verification' or 'recovery').

    Note:
        SMTP dispatch logic is proprietary and not included in this public version.
    """
    raise NotImplementedError("Proprietary implementation")


def send_error_alert(subject: str, body: str):
    """
    Send a 500 error alert to the platform operator's email.

    Called non-blocking from the 500 error handler. Errors in this function
    are silently suppressed.

    Args:
        subject: Error summary for the email subject.
        body: Full traceback for the email body.

    Note:
        Implementation is proprietary and not included in this public version.
    """
    raise NotImplementedError("Proprietary implementation")
