# CILeasing Automated Tests

A modern Playwright test automation framework using Python with Page Object Model (POM) design pattern.

## Features

- **Page Object Model**: Clean separation of test logic and page interactions
- **Environment Configuration**: Secure credential management via `.env` files
- **Type Hints**: Full type annotation for better IDE support and code quality
- **Pydantic Settings**: Type-safe configuration with validation
- **Pytest Integration**: Powerful test runner with fixtures and markers

## Project Structure

```
cileasing-automated-tests/
├── .github/                  # GitHub workflows
├── config/
│   ├── __init__.py
│   └── settings.py           # Pydantic settings loader
├── docs/                     # Documentation
├── pages/
│   ├── __init__.py
│   ├── base_page.py          # Base page with common methods
│   ├── home_page.py          # Home page object
│   └── login_page.py         # Login page object
├── tests_pages/
│   ├── __init__.py
│   ├── test_cases.py         # Additional test cases
│   └── test_user_logins.py   # Login tests
├── utils/
│   ├── __init__.py
│   └── constants.py          # Selectors and constants
├── venv/                     # Virtual environment (git-ignored)
├── .env                      # Environment variables (git-ignored)
├── .env.example              # Environment template
├── .gitignore
├── conftest.py               # Pytest fixtures (ROOT level)
├── DEPENDENCY_AUDIT.md
├── pyproject.toml            # Project configuration
├── README.md
└── requirements.txt          # Dependencies
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cileasing-automated-tests
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install chromium
   ```

5. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

## Configuration

Edit `.env` file with your settings:

```env
# Application URLs
BASE_URL=https://candileasing.netlify.app/
LOGIN_URL=https://candileasing.netlify.app/

# Test Credentials
TEST_USERNAME=your_email@example.com
TEST_PASSWORD=your_password

# Browser Settings
HEADLESS=false
SLOW_MO=0
TIMEOUT=30000

# Video Recording
RECORD_VIDEO=false
VIDEO_DIR=videos/
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run with verbose output
```bash
pytest -v
```

### Run specific test file
```bash
pytest tests_pages/test_user_logins.py
```

### Run tests by marker
```bash
pytest -m smoke           # Run smoke tests
pytest -m login           # Run login tests
pytest -m "smoke and login"  # Run tests with both markers
```

### Run tests in parallel
```bash
pip install pytest-xdist
pytest -n auto
```

### Generate HTML report
```bash
pytest --html=report.html --self-contained-html
```

## Writing Tests

### Using Page Object fixtures

```python
def test_login(home_page):
    home_page.go_to_home_page()
    home_page.login_user()
```

### Using custom credentials

```python
def test_login_custom(home_page):
    home_page.go_to_home_page()
    home_page.login_user(
        email="custom@example.com",
        password="custom_password"
    )
```

### Using markers

```python
import pytest

@pytest.mark.smoke
@pytest.mark.login
def test_critical_login(home_page):
    home_page.go_to_home_page()
    home_page.login_user()
```

## License

MIT License
