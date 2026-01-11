# Dependency Audit

## Last Updated
January 2025

## Core Dependencies

| Package | Version | Purpose | Security Status |
|---------|---------|---------|-----------------|
| playwright | >=1.40.0 | Browser automation | ✅ Current |
| pytest | >=8.0.0 | Test framework | ✅ Current |
| pytest-playwright | >=0.4.4 | Pytest integration | ✅ Current |
| pydantic | >=2.5.0 | Data validation | ✅ Current |
| pydantic-settings | >=2.1.0 | Settings management | ✅ Current |

## Optional Dependencies

| Package | Version | Purpose | Security Status |
|---------|---------|---------|-----------------|
| pytest-html | >=4.1.0 | HTML reports | ✅ Current |
| pytest-xdist | >=3.5.0 | Parallel execution | ✅ Current |
| black | >=24.0.0 | Code formatting | ✅ Current |
| ruff | >=0.1.0 | Linting | ✅ Current |
| mypy | >=1.8.0 | Type checking | ✅ Current |

## Audit Commands

```bash
# Check for vulnerabilities
pip-audit

# Update dependencies
pip install --upgrade -r requirements.txt

# Generate updated requirements
pip freeze > requirements.lock
```
