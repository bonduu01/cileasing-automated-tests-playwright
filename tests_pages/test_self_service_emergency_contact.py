import pytest
from playwright.sync_api import Page
from config import settings
import logging

from pages import SelfServicePage

logger = logging.getLogger(__name__)


class TestEmergencyContactPage:
    """Test suite for Self-Service functionalities."""

    @pytest.fixture(autouse=True)
    def setup_test_logging(self, request):
        """Log test setup and teardown."""
        test_name = request.node.name
        logger.info(f"\n{'#' * 80}")
        logger.info(f"🧪 STARTING TEST: {test_name}")
        logger.info(f"{'#' * 80}\n")
        yield

        logger.info(f"\n{'#' * 80}")
        logger.info(f"🏁 FINISHED TEST: {test_name}")
        logger.info(f"{'#' * 80}\n")

    @pytest.fixture(autouse=True)
    def setup(self, authenticated_page: Page):
        """Setup before each test - store page in self"""
        logger.info("📋 Authenticate User module")
        self.page = authenticated_page
        self.self_service_page = SelfServicePage(self.page)

        yield
        # Cleanup if needed

    @pytest.mark.regression
    def test_to_add_new_emergency_contact(self) -> None:
        """Test Add New emergency contact with debugging"""
        # Debug: Check current page
        logger.info(f"📍 Current URL: {self.page.url}")
        logger.info(f"📍 Page Title: {self.page.title()}")

        # Wait for page to be ready
        self.page.wait_for_load_state("domcontentloaded")

        # Debug: Check if Add Emergency Contact Button is visible
        from utils.constants import SELF_SERVICE_PAGE
        self_service_page = self.page.locator(SELF_SERVICE_PAGE.EMERGENCY_CONTACTS_BUTTON)

        logger.info(f"🔍 Add Emergency Contact Button visible: {self_service_page.is_visible()}")
        logger.info(f"🔍 Add Emergency Contact Button count: {self_service_page.count()}")

        if self_service_page.count() > 0:
            logger.info(f"🔍 Add Emergency Contact Button text: {self_service_page.text_content()}")

        # Click to add
        emergency_contacts_page = self.self_service_page.click_to_add_emergency_contacts_details()

        # Debug: Check navigation happened
        logger.info(f"📍 After click URL: {self.page.url}")
        emergency_contacts_page.create_new_emergency_contacts_details()
        logger.info("✅ Add Emergency Contact details created successful")

    @pytest.mark.regression
    def test_to_edit_new_emergency_contact(self) -> None:
        """Test edit emergency contact with debugging"""
        # Debug: Check current page
        logger.info(f"📍 Current URL: {self.page.url}")
        logger.info(f"📍 Page Title: {self.page.title()}")

        # Wait for page to be ready
        self.page.wait_for_load_state("domcontentloaded")

        # Debug: Check if Add Emergency Contact Button is visible
        from utils.constants import SELF_SERVICE_PAGE
        self_service_page = self.page.locator(SELF_SERVICE_PAGE.EMERGENCY_CONTACTS_BUTTON)

        logger.info(f"🔍 Add Emergency Contact Button visible: {self_service_page.is_visible()}")
        logger.info(f"🔍 Add Emergency Contact Button count: {self_service_page.count()}")

        if self_service_page.count() > 0:
            logger.info(f"🔍 Add Emergency Contact Button text: {self_service_page.text_content()}")

        # Click to add
        emergency_contacts_page = self.self_service_page.click_to_add_emergency_contacts_details()

        # Debug: Check navigation happened
        logger.info(f"📍 After click URL: {self.page.url}")
        emergency_contacts_page.create_new_emergency_contacts_details()
        logger.info("✅ Add Emergency Contact details created successful")
        emergency_contacts_page.wait(5000)
