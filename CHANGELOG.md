# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-01-XX

### Added
- **Complete class-based refactoring** with modular architecture
  - `MapPoster`: Main orchestrator class for poster generation
  - `Theme`: Theme management system with property validation
  - `Geocoder`: Location-to-coordinates conversion with caching
  - `Renderer`: Dedicated map visualization engine
  
- **Improved code organization**
  - Separated concerns into focused modules
  - Better testability with unit test suite
  - Type hints throughout codebase
  - Comprehensive docstrings

- **Enhanced command-line interface**
  - Improved argument parsing with argparse
  - Better error messages and validation
  - Theme listing functionality
  - Progress indicators

- **Better configuration management**
  - `RenderConfig` dataclass for rendering options
  - `Coordinates` dataclass for geocoding results
  - Centralized configuration handling

- **Test suite**
  - pytest-based unit tests
  - Fixtures for common test objects
  - Test coverage for all core modules

- **Documentation**
  - Comprehensive README with examples
  - Contributing guidelines (CONTRIBUTING.md)
  - Architecture documentation
  - API reference in docstrings

### Changed
- Refactored from monolithic script to package structure
- Geocoder now uses Nominatim with configurable user agent
- Theme system more flexible with JSON and dict loading
- Rendering separated from data fetching
- CLI completely rewritten with better UX

### Removed
- Legacy monolithic script approach
- Tight coupling between components
- Hardcoded configuration values

### Fixed
- Better error handling and recovery
- Proper resource cleanup
- Type checking with mypy

### Dependencies
- matplotlib>=3.5.0
- osmnx>=1.7.0
- networkx>=2.6
- requests>=2.25.0
- geopandas>=0.12.0
- shapely>=2.0.0

## Migration Guide from v1 to v2

### Command Line

**Before (v1):**
```bash
python create_map_poster.py --city "Paris" --country "France"
```

**After (v2):**
```bash
python -m maptoposter.cli --city "Paris" --country "France"
# or
maptoposter --city "Paris" --country "France"
```

### Python API

**Before (v1):**
```python
# Functions scattered in module
from create_map_poster import create_poster
create_poster(city, country, theme, ...)
```

**After (v2):**
```python
from maptoposter import MapPoster
poster = MapPoster()
output_path = poster.create_poster(city, country, theme_name=theme)
```

## [1.0.0] - Original Release

### Features
- Map poster generation for any city
- 17 built-in themes
- Customizable dimensions and zoom
- Multilingual support
- OpenStreetMap integration
- High-quality rendering (300 DPI)

---

## Versioning Policy

- **MAJOR** version for breaking changes
- **MINOR** version for new features
- **PATCH** version for bug fixes

## Future Roadmap

### v2.1.0 (Planned)
- Batch CSV processing
- POI overlay support
- Route highlighting

### v2.2.0 (Planned)
- REST API wrapper
- SVG/PDF export
- Web dashboard

### v3.0.0 (Future)
- Plugin system
- Multiple map providers
- Advanced styling options
- Cloud deployment support
