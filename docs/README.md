# py-ia-rom-logger

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-alpha-orange.svg)
![Coverage](https://img.shields.io/badge/coverage-89.82%25-brightgreen.svg)
![Tests](https://img.shields.io/badge/tests-97%20passed-success.svg)

> A professional logging library for Python projects with Rich console formatting and structured JSON file output.

Modern logging solution designed for automation and Python projects, providing beautiful console output for development and structured JSON logs for production analysis.

---

## ✨ Features

- **🎨 Rich Console Output**
  - Beautiful colored console logs with Rich library
  - Customizable themes for different log levels
  - Enhanced readability with styled formatting

- **📝 Structured JSON Logging**
  - JSON-formatted file output for easy parsing
  - Automatic emoji removal for legacy system compatibility
  - Compact traceback formatting to reduce noise

- **🔧 Production-Ready**
  - Singleton pattern for centralized log management
  - Automatic file rotation with configurable limits
  - Date-based directory organization (YYYY-MM/DD)
  - Timezone support with configurable TZ

- **🛡️ Exception Handling**
  - Automatic exception tracking with sys.excepthook
  - Thread exception capture (Python ≥3.8)
  - Detailed but compact traceback formatting

- **⚙️ Highly Configurable**
  - Environment variable configuration
  - Custom formatters and handlers
  - Flexible log levels and output formats

---

## 📦 Installation

### From Git (Development)

```bash
uv pip install git+https://github.com/Yharon/py-ia-rom-logger.git
```

### From Source

```bash
git clone https://github.com/Yharon/py-ia-rom-logger.git
cd py-ia-rom-logger
uv pip install -e .
```

### Dependencies

- Python ≥ 3.12
- rich ≥ 13.0.0
- python-json-logger ≥ 3.3.0
- textual ≥ 0.41.0
- pydantic ≥ 2.0.0
- tzdata ≥ 2025.2

---

## 🛠️ Development Setup

### Prerequisites

- Python ≥ 3.12
- uv package manager: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- direnv installed: `sudo apt install direnv`
- Environment variables configured in `~/.bashrc`:

  ```bash
  export DEV_ROOT="$HOME/dev"
  export RES_ROOT="$HOME/resources"
  export RES_ENVS="$RES_ROOT/python-venvs"
  export CONTEXTS_DIR="$DEV_ROOT/contexts/claude"

  # direnv hook
  eval "$(direnv hook bash)"
  ```

### Setup Development Environment

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Yharon/py-ia-rom-logger.git
   ```

2. **Navigate to project (direnv auto-activates):**

   ```bash
   cd py-ia-rom-logger
   direnv allow
   ```

That's it! **direnv automatically:**

- ✅ Activates Python virtual environment
- ✅ Configures external cache via environment variables
- ✅ Exports all project environment variables
- ✅ Loads project `.env` file

### Quick Navigation

**Use the `work` function (if configured):**

```bash
work py-ia-rom-logger  # Navigate + activate in one command
```

**Or navigate manually:**

```bash
cd ~/dev/projects/libs/py-ia-rom-logger
# Environment is automatically loaded by direnv
```

### Run Development Tasks

```bash
# Run tests (direct commands, no wrappers needed)
pytest              # Run all tests
pytest -v           # Verbose output
poe test           # Or use Poe task runner

# Code quality
ruff check .        # Linting
ruff format .       # Formatting
mypy src           # Type checking

# Combined checks
poe check          # lint + typecheck + test
```

### External Cache Structure

All cache files are stored outside the project in `$RES_ROOT/cache/py-ia-rom-logger/`:

```bash
$RES_ROOT/cache/py-ia-rom-logger/
├── .pytest_cache/      # Pytest cache
├── .mypy_cache/        # Mypy cache
├── .ruff_cache/        # Ruff cache
├── .uv_cache/          # UV package manager cache
├── htmlcov/            # Coverage HTML reports
├── pycache/            # Python bytecode cache
├── .coverage           # Coverage data
└── coverage.xml        # Coverage XML report
```

Tools automatically use these locations via environment variables (`PYTEST_CACHE_DIR`, `MYPY_CACHE_DIR`, etc.), keeping the project directory clean.

---

## 🚀 Quick Start

### Basic Usage

```python
from py_ia_rom_logger import LoggingManager

# Initialize logging manager (singleton)
manager = LoggingManager()
manager.setup_logging(level="DEBUG")

# Get logger instance
logger = manager.get_logger(__name__)

# Log messages
logger.debug("Debug information")
logger.info("Process started successfully")
logger.warning("Resource usage is high")
logger.error("Failed to connect to database")
logger.critical("System is shutting down")
```

### Exception Logging

```python
try:
    result = risky_operation()
except Exception as e:
    logger.exception("Operation failed")  # Includes full traceback
```

### Named Loggers

```python
# Create module-specific loggers
auth_logger = manager.get_logger("app.auth")
db_logger = manager.get_logger("app.database")

auth_logger.info("User authenticated")
db_logger.debug("Query executed: SELECT * FROM users")
```

---

## ⚙️ Configuration

### Environment Variables

Configure logging behavior via environment variables:

```bash
# Log directory (default: PROJECT_ROOT/logs)
LOG_DIR=/var/log/myapp

# Maximum log files to keep (default: 5)
MAX_FILES=10

# Robot/Process identification
ROBO_ID=robot_001
ROUND_ID=42

# Timezone (default: America/Sao_Paulo)
TIMEZONE=UTC

# Traceback configuration
TRACEBACKS_MAX_FRAMES=8
TRACEBACKS_EXTRA_LINES=3
TRACEBACKS_CONTEXT_LINES=3

# Environment type (default: DEV)
ENV=PROD
```

### Custom Formatters

```python
from py_ia_rom_logger.handlers import AvailableFormatters, AvailableFileFormatters

manager.setup_logging(
    console_formatter=AvailableFormatters.RICH,
    file_formatter=AvailableFileFormatters.JSON,
    level="INFO"
)
```

### Log File Structure

```bash
logs/
├── 2025-01/
│   ├── 15/
│   │   ├── 1_01_20250115_143025_01.log
│   │   ├── 1_01_20250115_150130_01.log
│   │   └── ...
│   └── 16/
│       └── ...
└── 2025-02/
    └── ...
```

**Filename pattern:** `{ROBO_ID}_{PART}_{DATE}_{TIME}_{ROUND_ID}.log`

### JSON Log Format

```json
{
  "timestamp": "2025-01-15T14:30:25.123456-03:00",
  "level": "INFO",
  "message": "Process completed successfully",
  "name": "app.worker",
  "pathname": "/path/to/script.py",
  "lineno": 42,
  "customargs": ["user_123", 456]
}
```

With exceptions:

```json
{
  "timestamp": "2025-01-15T14:30:25.123456-03:00",
  "level": "ERROR",
  "message": "Failed to process data",
  "exc_name": "ValueError",
  "exc_message": "Invalid input format",
  "exc_info": "Traceback (most recent call last):\n  File ...\n    ..."
}
```

---

## 🏗️ Architecture

### Module Overview

```bash
py_ia_rom_logger/
├── config/              # Configuration management
│   ├── config.py       # Settings class with env variables
│   └── decorators.py   # Singleton pattern decorator
│
├── models/             # Data models
│   ├── _log_model.py          # Base log model
│   ├── console_log_model.py   # Console-specific model
│   └── file_log_model.py      # File-specific model
│
├── handlers/           # Log handlers
│   ├── console_handler.py     # Rich console handler
│   └── file_handler.py        # JSON file handler
│
├── helpers/            # Utility helpers
│   ├── formatters/
│   │   ├── console_rich_formatter.py      # Rich console formatter
│   │   ├── file_json_formatter.py         # JSON file formatter
│   │   └── tracebacks/
│   │       ├── compact_traceback_formatter.py       # Compact tracebacks
│   │       └── console_rich_traceback_formatter.py  # Rich tracebacks
│   └── system_info_helper.py  # System information
│
└── services/           # Core services
    ├── logging_manager_service.py  # Main logging manager
    └── file_manager_service.py     # File rotation & cleanup
```

### Key Components

- **LoggingManager**: Singleton service that coordinates all handlers
- **Settings**: Centralized configuration with environment variable support
- **SafeJsonFormatter**: JSON formatter with emoji removal and UTF-8 safety
- **FileManagerService**: Handles log rotation and directory structure
- **CompactTracebackFormatter**: Reduces traceback noise while preserving info

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_services/test_logging_manager.py

# Run tests by marker
pytest -m unit
pytest -m integration
pytest -m "not slow"

# Verbose output
pytest -v
```

### Using Poe Task Runner

```bash
# Run tests
poe test

# Run with coverage report
poe test-cov

# Run fast tests only (skip slow markers)
poe test-fast
```

### Coverage Report

Current coverage: **89.82%** (97 tests passing)

```bash
# Generate coverage report
pytest --cov=py_ia_rom_logger --cov-report=html

# Open in browser
open htmlcov/index.html
```

### Test Structure

```bash
tests/
├── conftest.py                 # Shared fixtures
├── test_config/               # Configuration tests
├── test_models/               # Model tests
├── test_helpers/              # Helper tests
├── test_handlers/             # Handler tests
├── test_services/             # Service tests
└── test_integration/          # E2E integration tests
```

---

## 🛠️ Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/Yharon/py-ia-rom-logger.git
cd py-ia-rom-logger

# Install in editable mode with dev dependencies
uv pip install -e ".[dev]"
```

### Development Tools

```bash
# Linting
poe lint              # Check code with Ruff
poe format            # Format code with Ruff
poe fix               # Auto-fix linting issues

# Type checking
poe typecheck         # Run mypy

# Run all checks
poe check             # lint + typecheck + test

# Clean build artifacts
poe clean
```

### Code Quality Standards

- **Python**: 3.12+
- **Style**: PEP 8 (enforced by Ruff)
- **Docstrings**: Google Style
- **Type Hints**: Required for public APIs
- **Imports**: Sorted via Ruff (isort-compatible)
- **Line Length**: 88 characters (Black-compatible)

### Commit Guidelines

Follow conventional commits format:

```bash
feat: add new feature
fix: fix bug in logger
docs: update README
test: add tests for handlers
refactor: improve code structure
chore: update dependencies
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Yharon Coutinho**

- Email: <coutinho@ia-rom.com>
- GitHub: [@Yharon](https://github.com/Yharon)
- Organization: CORE

---

## 🔗 Links

- [Repository](https://github.com/Yharon/py-ia-rom-logger)
- [Changelog](https://github.com/Yharon/py-ia-rom-logger/blob/main/CHANGELOG.md)
- [Issues](https://github.com/Yharon/py-ia-rom-logger/issues)

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/Yharon">Yharon Coutinho</a>
</p>
