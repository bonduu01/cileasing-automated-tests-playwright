from playwright.sync_api import Page

from pages.base_page import BasePage
from config import settings
from utils.constants import ADD_BANK_DETAILS_PAGE, ADD_BVN_PAGE, ADD_IDENTITY_PAGE
from utils.decorators import log_method
import logging

logger = logging.getLogger(__name__)


class AddIdentityPage(BasePage):
    """Page Object for the Login Page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @log_method
    def create_new_identity(self, test_identity_type: str | None = None, test_identity_id: str | None = None,
                            test_issued_date: str | None = None, test_expiry_date: str | None = None) -> None:
        """ Add  new identity """
        test_identity_type = test_identity_type or settings.test_identity_type
        test_identity_id = test_identity_id or settings.test_identity_id
        test_issued_date = test_issued_date or settings.test_issued_date
        test_expiry_date = test_expiry_date or settings.test_expiry_date

        logger.info(f"🔐 Attempting to create identity using: {test_identity_id}")

        self.ant_select_option(
            ADD_IDENTITY_PAGE.IDENTITY_TYPE_DROPDOWN,
            ADD_IDENTITY_PAGE.IDENTITY_TYPE
        )

        self.fill_input(ADD_IDENTITY_PAGE.IDENTITY_ID, test_identity_id)
        self.ant_select_date_picker(ADD_IDENTITY_PAGE.EXPIRY_DATE_SELECTOR, test_expiry_date)
        self.ant_select_date_picker(ADD_IDENTITY_PAGE.ISSUED_DATE_SELECTOR, test_issued_date)
        self.click_element(ADD_IDENTITY_PAGE.ADD_IDENTITY_BUTTON)
        logger.info(f"✅ Identity Created Successfully")
