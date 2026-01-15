import pytest
from pages import EditSelfServicePage, SelfServicePage
from playwright.sync_api import Page
from config import settings


class TestEditSelfServicePage:
    """Test suite for Self-Service functionalities."""

    @pytest.fixture(autouse=True)
    def setup(self, authenticated_page: Page):
        """Setup before each test - store page in self"""
        self.page = authenticated_page
        self.self_service_page = SelfServicePage(self.page)
        self.edit_self_service_page = EditSelfServicePage(self.page)
        yield
        # Cleanup if needed

    @pytest.mark.regression
    def test_edit_personal_details(self) -> None:
        """Test editing personal details"""

        self.self_service_page.click_to_edit_personal_date_details()

        self.edit_self_service_page.edit_personal_data_details(
            other_name=settings.test_other_name,
            job_title=settings.test_job_title
        )

        # Better wait strategy
        self.page.wait_for_load_state("networkidle", timeout=10000)

        # Verify changes
        # expect(self.page.locator("input[name='otherName']")).to_have_value(
        #     settings.test_other_name
        # )
