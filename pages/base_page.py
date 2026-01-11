"""
Base Page Object providing common interactions for all page objects.
"""

from __future__ import annotations

import os
import re
from typing import TYPE_CHECKING

from playwright.sync_api import Page, expect, Locator, Download

if TYPE_CHECKING:
    from playwright.sync_api import Response


class BasePage:
    """Base class for all Page Objects with common functionality."""

    def __init__(self, page: Page) -> None:
        self.page = page

    # --- Navigation ---

    def navigate_to(self, url: str, wait_until: str = "domcontentloaded") -> Response | None:
        """Navigate to a URL and wait for the specified load state."""
        return self.page.goto(url, wait_until=wait_until)

    def reload(self, wait_until: str = "domcontentloaded") -> Response | None:
        """Reload the current page."""
        return self.page.reload(wait_until=wait_until)

    def go_back(self, wait_until: str = "domcontentloaded") -> Response | None:
        """Navigate back in browser history."""
        return self.page.go_back(wait_until=wait_until)

    # --- Element Interaction ---

    def click_element(self, selector: str, **kwargs) -> None:
        """Click an element identified by selector."""
        self.page.click(selector, **kwargs)

    def fill_input(self, selector: str, value: str) -> None:
        """Fill an input field with the specified value."""
        self.page.fill(selector, value)

    def type_text(self, selector: str, text: str, delay: float = 0) -> None:
        """Type text into an element character by character."""
        self.page.type(selector, text, delay=delay)

    def clear_input(self, selector: str) -> None:
        """Clear the content of an input field."""
        self.page.fill(selector, "")

    def check_checkbox(self, selector: str) -> None:
        """Check a checkbox or radio button."""
        self.page.locator(selector).check()

    def uncheck_checkbox(self, selector: str) -> None:
        """Uncheck a checkbox."""
        self.page.locator(selector).uncheck()

    def select_dropdown_option(
        self, selector: str, value: str | None = None, label: str | None = None
    ) -> list[str]:
        """Select an option from a dropdown."""
        locator = self.page.locator(selector)
        if label:
            return locator.select_option(label=label)
        return locator.select_option(value=value)

    def upload_file(self, selector: str, file_path: str | list[str]) -> None:
        """Upload file(s) to a file input."""
        self.page.set_input_files(selector, file_path)

    def hover_element(self, selector: str) -> None:
        """Hover over an element."""
        self.page.hover(selector)

    def press_key(self, selector: str, key: str) -> None:
        """Press a key while focused on an element."""
        self.page.press(selector, key)

    # --- Element Getters ---

    def get_locator(self, selector: str) -> Locator:
        """Get a locator for the specified selector."""
        return self.page.locator(selector)

    def get_role(self, role: str, name: str | None = None, **kwargs) -> Locator:
        """Get element by ARIA role."""
        return self.page.get_by_role(role, name=name, **kwargs)

    def get_by_text(self, text: str, exact: bool = False) -> Locator:
        """Get element by text content."""
        return self.page.get_by_text(text, exact=exact)

    def get_by_label(self, label: str, exact: bool = False) -> Locator:
        """Get element by associated label."""
        return self.page.get_by_label(label, exact=exact)

    def get_by_placeholder(self, placeholder: str, exact: bool = False) -> Locator:
        """Get element by placeholder attribute."""
        return self.page.get_by_placeholder(placeholder, exact=exact)

    def get_by_test_id(self, test_id: str) -> Locator:
        """Get element by data-testid attribute."""
        return self.page.get_by_test_id(test_id)

    # --- Text Extraction ---

    def get_value_from_selector(self, selector: str) -> str:
        """Get the text content of an element."""
        text = self.page.locator(selector).first.text_content()
        return text.strip() if text else ""

    def get_inner_text(self, selector: str) -> str:
        """Get the inner text of an element."""
        return self.page.locator(selector).first.inner_text()

    def get_input_value(self, selector: str) -> str:
        """Get the value of an input element."""
        return self.page.locator(selector).input_value()

    def get_attribute(self, selector: str, attribute: str) -> str | None:
        """Get an attribute value from an element."""
        return self.page.locator(selector).first.get_attribute(attribute)

    # --- Assertions ---

    def verify_title(self, expected_title: str | re.Pattern) -> None:
        """Assert the page title matches expected value."""
        expect(self.page).to_have_title(expected_title)

    def verify_url(self, expected_url: str | re.Pattern) -> None:
        """Assert the page URL matches expected value."""
        expect(self.page).to_have_url(expected_url)

    def verify_element_visible(self, selector: str, timeout: float | None = None) -> None:
        """Assert an element is visible."""
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout)

    def verify_element_hidden(self, selector: str, timeout: float | None = None) -> None:
        """Assert an element is hidden."""
        expect(self.page.locator(selector)).to_be_hidden(timeout=timeout)

    def verify_element_is_enabled(self, selector: str) -> None:
        """Assert an element is enabled."""
        expect(self.page.locator(selector)).to_be_enabled()

    def verify_element_is_disabled(self, selector: str, timeout: float | None = None) -> None:
        """Assert an element is disabled."""
        locator = self.page.locator(selector)
        locator.wait_for(state="attached", timeout=timeout or 10000)
        expect(locator).to_be_disabled()

    def verify_selector_to_have_text(self, selector: str, expected_text: str | re.Pattern) -> None:
        """Assert an element has exact text."""
        expect(self.page.locator(selector)).to_have_text(expected_text)

    def verify_text_visible(self, text: str) -> None:
        """Assert text is visible on the page."""
        expect(self.page.get_by_text(text)).to_be_visible()

    def verify_has_text_visible(self, selector: str, text: str) -> None:
        """Assert element with specific text is visible."""
        expect(self.page.locator(selector, has_text=text)).to_be_visible()

    def verify_element_to_contain_text(
        self, selector: str, expected_text: str | re.Pattern
    ) -> None:
        """Assert an element contains text."""
        expect(self.page.locator(selector)).to_contain_text(expected_text)

    def verify_element_has_value(self, selector: str, expected_value: str | re.Pattern) -> None:
        """Assert an input has the expected value."""
        expect(self.page.locator(selector)).to_have_value(expected_value)

    def verify_element_checked(self, selector: str) -> None:
        """Assert a checkbox/radio is checked."""
        expect(self.page.locator(selector)).to_be_checked()

    def verify_element_not_checked(self, selector: str) -> None:
        """Assert a checkbox/radio is not checked."""
        expect(self.page.locator(selector)).not_to_be_checked()

    # --- Waiting ---

    def wait_for_selector(
        self, selector: str, state: str = "visible", timeout: float | None = None
    ) -> Locator:
        """Wait for a selector to reach the specified state."""
        self.page.wait_for_selector(selector, state=state, timeout=timeout)
        return self.page.locator(selector)

    def wait_for_url(self, url: str | re.Pattern, timeout: float | None = None) -> None:
        """Wait for navigation to a URL."""
        self.page.wait_for_url(url, timeout=timeout)

    def wait_for_load_state(self, state: str = "load") -> None:
        """Wait for a specific load state."""
        self.page.wait_for_load_state(state)

    def wait(self, milliseconds: float) -> None:
        """Wait for a specified duration (use sparingly)."""
        self.page.wait_for_timeout(milliseconds)

    # --- Scrolling ---

    def scroll_to_element(self, selector: str) -> None:
        """Scroll element into view."""
        self.page.locator(selector).scroll_into_view_if_needed()

    def scroll_to_txt_via_element(self, selector: str, text: str) -> None:
        """Scroll to an element containing specific text."""
        self.page.locator(selector, has_text=text).scroll_into_view_if_needed()

    def scroll_down(self) -> None:
        """Scroll to the bottom of the page."""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_to_top(self) -> None:
        """Scroll to the top of the page."""
        self.page.evaluate("window.scrollTo(0, 0)")

    # --- Downloads ---

    def click_and_verify_download(
        self,
        selector: str,
        save_path: str,
        expected_extensions: tuple[str, ...] = (".txt", ".pdf", ".csv", ".xlsx"),
    ) -> Download:
        """Click an element and handle the resulting file download."""
        with self.page.expect_download() as download_info:
            self.click_element(selector)

        download = download_info.value
        download.save_as(save_path)

        # Validate download
        actual_path = download.path()
        assert actual_path and os.path.exists(actual_path), (
            f"Downloaded file not found at {actual_path}"
        )

        filename = download.suggested_filename
        assert filename.endswith(expected_extensions), (
            f"Unexpected file type: {filename}, expected one of {expected_extensions}"
        )

        print(f"Download successful: {actual_path}")
        return download

    # --- Screenshots ---

    def screenshot(self, path: str, full_page: bool = False) -> bytes:
        """Take a screenshot of the page."""
        return self.page.screenshot(path=path, full_page=full_page)

    def screenshot_element(self, selector: str, path: str) -> bytes:
        """Take a screenshot of a specific element."""
        return self.page.locator(selector).screenshot(path=path)

    # --- JavaScript Execution ---

    def evaluate(self, expression: str):
        """Execute JavaScript in the page context."""
        return self.page.evaluate(expression)

    # --- State Checks ---

    def is_visible(self, selector: str) -> bool:
        """Check if an element is visible."""
        return self.page.locator(selector).is_visible()

    def is_enabled(self, selector: str) -> bool:
        """Check if an element is enabled."""
        return self.page.locator(selector).is_enabled()

    def is_checked(self, selector: str) -> bool:
        """Check if a checkbox/radio is checked."""
        return self.page.locator(selector).is_checked()

    def count_elements(self, selector: str) -> int:
        """Count the number of elements matching the selector."""
        return self.page.locator(selector).count()
