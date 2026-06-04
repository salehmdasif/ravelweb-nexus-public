"""
File upload service: validates and saves user-uploaded files (logos, profile photos).

Validates file type and size before writing to disk.
"""

import os


def save_upload(file_obj, upload_folder: str, allowed_extensions: set) -> str | None:
    """
    Validate and save an uploaded file to disk.

    Args:
        file_obj: Flask request.files file object.
        upload_folder: Absolute path to the upload destination directory.
        allowed_extensions: Set of permitted file extensions, e.g. {'jpg', 'png'}.

    Returns:
        str | None: The saved filename on success, None if the file is invalid.

    Note:
        File validation and naming logic is proprietary and not included in
        this public version.
    """
    raise NotImplementedError("Proprietary implementation")
