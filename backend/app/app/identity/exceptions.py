
class IdentityException(Exception):
    """Raised when an identity exception occurs"""
    pass

class AuthenticationNotFound(IdentityException):
    """Raised when authentication is not found in Pizzly"""
    pass

class InvalidAuthentication(IdentityException):
    """Raised when external identity provider returns invalid authentication response"""
    pass