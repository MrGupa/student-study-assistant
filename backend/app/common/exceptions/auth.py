class EmailAlreadyRegisteredError(Exception):
    """Raised when an email address is already registered."""


class InvalidCredentialsError(Exception):
    """Raised when login credentials are invalid."""


class AccountInactiveError(Exception):
    """Raised when an inactive account attempts to authenticate."""
