import pytest
from pages import SelfServicePage
from playwright.sync_api import Page


class TestSelfServiceModule:
    """Test suite for Self-Service functionalities."""

    @pytest.mark.regression
    def test_edit_personal_details(self, authenticated_page: Page) -> None:
        self_service_page = SelfServicePage(authenticated_page)
        self_service_page.wait(5000)
