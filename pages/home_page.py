"""
Home Page Object for the CAndILeasing application.
"""

from playwright.sync_api import Page

from pages.base_page import BasePage
from config import settings
from utils.constants import HOME_PAGE, LOGIN_PAGE


class HomePage(BasePage):
    """Page Object for the Home Page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.url = settings.base_url

    def go_to_home_page(self) -> None:
        """Navigate to the home page."""
        self.navigate_to(self.url)

    def verify_home_page_loads(self) -> None:
        """Verify the home page has loaded correctly."""
        self.verify_title(HOME_PAGE.TITLE)
        self.verify_element_is_disabled(LOGIN_PAGE.PASSWORD_DISABLED)

    def login_user(self, email: str | None = None, password: str | None = None) -> None:
        """
        Perform login with provided or default credentials.

        Args:
            email: User email (defaults to TEST_USERNAME from .env)
            password: User password (defaults to TEST_PASSWORD from .env)
        """
        email = email or settings.test_username
        password = password or settings.test_password

        self.fill_input(LOGIN_PAGE.EMAIL_INPUT, email)
        self.fill_input(LOGIN_PAGE.PASSWORD_INPUT, password)
        self.click_element(LOGIN_PAGE.SUBMIT_BUTTON)

    def enter_email(self, email: str) -> None:
        """Enter email address."""
        self.fill_input(LOGIN_PAGE.EMAIL_INPUT, email)

    def enter_password(self, password: str) -> None:
        """Enter password."""
        self.fill_input(LOGIN_PAGE.PASSWORD_INPUT, password)

    def click_login_button(self) -> None:
        """Click the login button."""
        self.click_element(LOGIN_PAGE.SUBMIT_BUTTON)

    def verify_login_form_visible(self) -> None:
        """Verify login form elements are visible."""
        self.verify_element_visible(LOGIN_PAGE.EMAIL_INPUT)
        self.verify_element_visible(LOGIN_PAGE.PASSWORD_INPUT)
        self.verify_element_visible(LOGIN_PAGE.SUBMIT_BUTTON)
