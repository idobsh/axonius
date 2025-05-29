# Axonius Airbnb Automation Project

## Overview

This project automates Airbnb search, booking, and validation workflows using Python, Playwright, and Pytest.
It is structured using the Page Object Model for maintainability and clarity.

---

## Project Structure

```
axonius/
├── helpers/              # Utility functions (date, string, price, etc.)
├── pages/                # Page objects and UI components
│   ├── modals/
│   └── ui_components/
├── tests/                # Test cases and test data
│   ├── artifacts/        # Test run artifacts (ignored by git)
│   └── tests_data/
├── requirements.txt      # Python dependencies
├── Makefile              # Automation commands
├── Dockerfile            # Docker setup for CI/local runs
└── .pre-commit-config.yaml # Pre-commit hooks config
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd axonius
```

### 2. Install Dependencies

```bash
make install
```

### 3. Install Playwright Browsers

```bash
make playwright
```

### 4. Run Tests

```bash
make test
```

Or do all at once:

```bash
make all
```

---

## Docker Usage

Build and run tests in Docker for a consistent environment:

```bash
docker build -t axonius-airbnb .
docker run --rm axonius-airbnb
```

---

## Artifacts

- Test artifacts (such as JSON files with card data) are saved in `tests/artifacts/`.
- This folder is **gitignored** by default.

---

## Customization

- **Test Data:**
  Edit or add files in `tests/tests_data/` to change destinations, guests, etc.
