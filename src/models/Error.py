class RecordNotFoundError(Exception):
    """Should be raised when not finding a record is critical and will lead to follow-up errors."""

class RecordCreationError(Exception):
    """Should be raised when not being able to create a record is critical and will lead to follow-up errors."""