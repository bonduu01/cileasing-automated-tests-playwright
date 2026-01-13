"""
Pytest configuration and fixtures for Playwright tests.
Located at root directory for project-wide fixture access.
Optimized for CI/CD with Allure reporting integration.
"""

import os
from pathlib import Path
from typing import Generator
from datetime import datetime

import pytest
import allure
from playwright.sync_api import (
    Playwright,
    Browser,
    BrowserContext,
    Page,
    sync_playwright,
)

from config import settings
from pages import HomePage, LoginPage


# --- Core Playwright Fixtures ---


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """Session-scoped Playwright instance."""
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Generator[Browser, None, None]:
    """
    Session-scoped browser instance.
    Browser is created once and reused across all tests.
    Optimized for CI environment.
    """
    # Check if running in CI
    is_ci = os.getenv("CI", "false").lower() == "true"

    # Browser launch args for CI optimization
    launch_args = {
        "headless": settings.headless,
        "slow_mo": settings.slow_mo,
    }

    # Add CI-specific optimizations
    if is_ci:
        launch_args["args"] = [
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage",  # Overcome limited resource problems
            "--no-sandbox",  # Required for Docker/CI environments
        ]

    browser = playwright_instance.chromium.launch(**launch_args)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """
    Function-scoped browser context.
    Each test gets an isolated context (cookies, storage, etc.).
    With screenshot capture on failure.
    """
    context_options = {
        "accept_downloads": True,
        "viewport": {"width": 1920, "height": 1080},  # Standard viewport for consistency
    }

    # Add video recording if enabled (disabled in CI by default)
    if settings.record_video:
        context_options["record_video_dir"] = settings.video_dir

    context = browser.new_context(**context_options)
    context.set_default_timeout(settings.timeout)

    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """
    Function-scoped page instance.
    Each test gets a fresh page with automatic screenshot on failure.
    """
    page = context.new_page()
    yield page
    page.close()


# --- Page Object Fixtures ---


@pytest.fixture
def home_page(page: Page) -> HomePage:
    """HomePage fixture with Allure step tracking."""
    with allure.step("Initialize HomePage"):
        return HomePage(page)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """LoginPage fixture with Allure step tracking."""
    with allure.step("Initialize LoginPage"):
        return LoginPage(page)


# --- Utility Fixtures ---


@pytest.fixture
def authenticated_page(page: Page) -> Generator[Page, None, None]:
    """
    Page fixture that is already authenticated.
    Useful for tests that require a logged-in state.
    """
    with allure.step("Authenticate user"):
        login_page = LoginPage(page)
        login_page.go_to_login_page()
        login_page.login_user()
        # Add any post-login waits or verifications here
    yield page


# --- Pytest Hooks ---


def pytest_configure(config):
    """Configure custom pytest markers and Allure environment."""
    # Custom markers
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "login: mark test as login-related")
    config.addinivalue_line("markers", "slow: mark test as slow running")

    # Set up Allure environment info if not already done by workflow
    allure_results_dir = Path("allure-results")
    if allure_results_dir.exists():
        env_props = allure_results_dir / "environment.properties"
        if not env_props.exists():
            with open(env_props, "w") as f:
                f.write(f"Browser=chromium\n")
                f.write(f"Headless={settings.headless}\n")
                f.write(f"Python.Version={os.sys.version.split()[0]}\n")
                f.write(f"Test.Environment={'CI' if os.getenv('CI') else 'Local'}\n")


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on markers or config."""
    # Add smoke marker to tests that don't have it
    # This helps with test categorization in Allure
    for item in items:
        # Auto-add login marker for tests with "login" in name
        if "login" in item.nodeid.lower() and "login" not in [m.name for m in item.iter_markers()]:
            item.add_marker(pytest.mark.login)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture screenshots and page content on test failure.
    This hook runs after each test phase (setup, call, teardown).
    """
    outcome = yield
    report = outcome.get_result()

    # Only process on test failure during the call phase
    if report.when == "call" and report.failed:
        # Get the page fixture if it exists
        page = None
        for fixture_name in item.fixturenames:
            if fixture_name == "page":
                page = item.funcargs.get("page")
                break

        if page:
            # Create screenshots directory
            screenshot_dir = Path("test-results/screenshots")
            screenshot_dir.mkdir(parents=True, exist_ok=True)

            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name.replace("/", "_").replace("::", "_")
            screenshot_path = screenshot_dir / f"{test_name}_{timestamp}.png"

            try:
                # Capture screenshot
                page.screenshot(path=str(screenshot_path), full_page=True)

                # Attach to Allure report
                with open(screenshot_path, "rb") as image_file:
                    allure.attach(
                        image_file.read(),
                        name=f"Screenshot: {test_name}",
                        attachment_type=allure.attachment_type.PNG
                    )

                # Also attach page HTML for debugging
                html_content = page.content()
                allure.attach(
                    html_content,
                    name=f"Page HTML: {test_name}",
                    attachment_type=allure.attachment_type.HTML
                )

                # Attach console logs if available
                console_logs = []
                page.on("console", lambda msg: console_logs.append(f"{msg.type}: {msg.text}"))
                if console_logs:
                    allure.attach(
                        "\n".join(console_logs[-50:]),  # Last 50 logs
                        name=f"Console Logs: {test_name}",
                        attachment_type=allure.attachment_type.TEXT
                    )

            except Exception as e:
                # Don't fail the test if screenshot capture fails
                print(f"⚠️ Warning: Could not capture screenshot: {e}")


def pytest_runtest_setup(item):
    """Run before each test - add test metadata to Allure."""
    # Add test metadata to Allure
    allure.dynamic.description(f"Test: {item.name}")
    allure.dynamic.testcase(item.nodeid)

    # Add markers as labels
    for marker in item.iter_markers():
        if marker.name in ["smoke", "regression", "login", "slow"]:
            allure.dynamic.tag(marker.name)
            allure.dynamic.label("test_type", marker.name)

    # Add suite and sub-suite based on file structure
    test_path = Path(item.fspath)
    allure.dynamic.suite(test_path.parent.name)
    allure.dynamic.sub_suite(test_path.stem)


def pytest_runtest_call(item):
    """Run during test execution - log test info."""
    print(f"\n{'='*80}")
    print(f"🧪 Executing: {item.name}")
    print(f"📝 Location: {item.nodeid}")
    print(f"{'='*80}\n")


@pytest.hookimpl(tryfirst=True)
def pytest_exception_interact(node, call, report):
    """Capture additional debug info on exception."""
    if report.failed:
        # Log the exception details
        if call.excinfo:
            with allure.step(f"Exception: {call.excinfo.typename}"):
                allure.attach(
                    str(call.excinfo.value),
                    name="Exception Details",
                    attachment_type=allure.attachment_type.TEXT
                )


# --- Session Fixtures for Cleanup ---


@pytest.fixture(scope="session", autouse=True)
def cleanup_old_screenshots():
    """Clean up old screenshots at session start."""
    screenshot_dir = Path("test-results/screenshots")
    if screenshot_dir.exists():
        # Remove screenshots older than 7 days (optional, adjust as needed)
        import time
        current_time = time.time()
        for screenshot in screenshot_dir.glob("*.png"):
            try:
                file_age = current_time - screenshot.stat().st_mtime
                if file_age > 7 * 24 * 3600:  # 7 days in seconds
                    screenshot.unlink()
            except Exception:
                pass


@pytest.fixture(scope="session", autouse=True)
def log_test_environment():
    """Log test environment at session start."""
    print("\n" + "="*80)
    print("🔧 Test Environment Configuration")
    print("="*80)
    print(f"Environment: {'CI' if os.getenv('CI') else 'Local'}")
    print(f"Base URL: {settings.base_url}")
    print(f"Headless: {settings.headless}")
    print(f"Browser: chromium")
    print(f"Timeout: {settings.timeout}ms")
    print(f"Python: {os.sys.version.split()[0]}")

    if os.getenv("CI"):
        print(f"GitHub Run: #{os.getenv('GITHUB_RUN_NUMBER', 'N/A')}")
        print(f"Branch: {os.getenv('GITHUB_REF_NAME', 'N/A')}")
        print(f"Commit: {os.getenv('GITHUB_SHA', 'N/A')[:7]}")

    print("="*80 + "\n")
    yield

    print("\n" + "="*80)
    print("✅ Test Session Complete")
    print("="*80 + "\n")