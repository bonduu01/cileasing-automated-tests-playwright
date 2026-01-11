"""
Page selectors and UI constants.
Credentials and URLs should be loaded from .env via config/settings.py
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class HomePageSelectors:
    """Selectors for the Home Page."""
    TITLE: str = "CAndILeasing"


@dataclass(frozen=True)
class LoginPageSelectors:
    """Selectors for the Login Page."""
    EMAIL_INPUT: str = 'input[name="email"]'
    PASSWORD_INPUT: str = 'input[name="password"]'
    SUBMIT_BUTTON: str = 'button[type="submit"][buttontype="primary"]'
    PASSWORD_DISABLED: str = "input[name='password'][type='password']"


# Create singleton instances
HOME_PAGE = HomePageSelectors()
LOGIN_PAGE = LoginPageSelectors()
