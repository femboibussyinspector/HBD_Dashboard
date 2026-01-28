"""
Validation utility functions for input validation.
"""
import re


def is_valid_email(email):
    """
    Validate email format using regex.
    
    Args:
        email: Email string to validate
        
    Returns:
        bool: True if email format is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None


def is_valid_password(password):
    """
    Validate password strength.
    
    Requirements:
        - At least 8 characters
        - Contains at least one letter
        - Contains at least one number
    
    Args:
        password: Password string to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, None
