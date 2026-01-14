"""
Home Page Object for the CAndILeasing application.
"""

from playwright.sync_api import Page

from pages.home_page import HomePage
from pages.base_page import BasePage
from config import settings
from utils.constants import SELF_SERVICE_PAGE


class SelfServicePage(BasePage):
    """Page Object for the Home Page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.url = settings.self_service_url

    def verify_self_service_page_loads(self) -> None:
        """Verify the self-service page has loaded correctly."""
        self.verify_element_visible(SELF_SERVICE_PAGE.PERSONAL_NAME)

    def click_on_user_profile(self) -> None:
        """Click on the user profile icon"""
        self.click_element(SELF_SERVICE_PAGE.MM_PROFILE)

    def click_to_logout(self) -> HomePage:
        """Click on the logout button"""
        self.click_to_logout()
        return HomePage(self.page)
