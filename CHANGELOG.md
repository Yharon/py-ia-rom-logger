# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-10-12

### Added

- **Core Logging Features**
  - Singleton LoggingManager for centralized log management
  - Rich console output with beautiful colored formatting
  - Structured JSON file logging for production analysis
  - Automatic exception tracking via sys.excepthook
  - Thread exception capture (Python ≥3.8)
  - Named logger support for module-specific logging

- **File Management**
  - Automatic log rotation with configurable limits
  - Date-based directory organization (YYYY-MM/DD)
  - Intelligent filename pattern: `{ROBO_ID}_{PART}_{DATE}_{TIME}_{ROUND_ID}.log`
  - FileManagerService for handling log lifecycle

- **Formatters & Handlers**
  - SafeJsonFormatter with emoji removal for legacy system compatibility
  - CompactTracebackFormatter to reduce noise while preserving info
  - Rich console formatter with customizable themes
  - Console and file handlers with independent configuration

- **Configuration**
  - Environment variable-based configuration
  - Timezone support (configurable via TZ env var)
  - Pydantic models for type-safe log records
  - Decorator-based singleton pattern

- **Testing & Quality**
  - Comprehensive test suite with 97 tests
  - ~90% code coverage
  - pytest configuration with markers (unit, integration, slow)
  - Ruff for linting and formatting
  - mypy for type checking

- **Development Tools**
  - Poe the Poet task runner for common operations
  - direnv integration for environment management
  - External cache configuration (pytest, mypy, ruff)
  - Debug support with debugpy

- **Documentation**
  - Complete README with usage examples
  - Architecture documentation
  - Development setup guide
  - API documentation via docstrings

### Changed

- Updated dependencies to remove unused `textual` library
- Improved project description to better reflect actual functionality
- Optimized keywords for better discoverability

### Fixed

- Configuration initialization and debug print functionality
- Import ordering across all modules
- Cache and coverage reporting paths

## [Unreleased]

### Planned Features

- Custom log level colors configuration
- Log streaming support
- Performance optimizations for high-volume logging
- Additional output formats (CSV, XML)
- Web dashboard for log visualization

---

**Legend:**
- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security fixes

[0.1.0]: https://github.com/Yharon/py-ia-rom-logger/releases/tag/v0.1.0
