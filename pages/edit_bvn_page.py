from playwright.sync_api import Page

from pages.base_page import BasePage
from config import settings
from utils.constants import ADD_BVN_PAGE, EDIT_BVN_PAGE
from utils.decorators import log_method
import logging

logger = logging.getLogger(__name__)


class EditBnvPage(BasePage):
    """Page Object for the Login Page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @log_method
    def edit_bvn(self, test_bvn_number: str | None = None) -> None:
        """ edit bvn number """
        test_bvn_number = test_bvn_number or settings.test_bvn_number1

        logger.info(f"🔐 Attempting to create bank details using: {test_bvn_number}")

        self.clear_input(EDIT_BVN_PAGE.EDIT_INPUT)
        self.fill_input(EDIT_BVN_PAGE.EDIT_INPUT, test_bvn_number)
        self.verify_input_value_length(EDIT_BVN_PAGE.EDIT_INPUT, 11)
        self.verify_element_has_value(EDIT_BVN_PAGE.EDIT_INPUT, test_bvn_number)
        logger.info(f"✅ Bank VPN: {test_bvn_number} edited and verified")
        self.click_element(EDIT_BVN_PAGE.EDIT_BVN_BUTTON)
        logger.info(f"✅ Bank Created Successfully")
