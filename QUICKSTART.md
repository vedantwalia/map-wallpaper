# MapToPoster 2.0 - Quick Start Guide

## Installation & First Run

### 1. Navigate to Project

```bash
cd /Users/vedantwalia/map-test
```

### 2. Install Dependencies

```bash
# Option A: Using pip + venv (Recommended for MacOS)
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Option B: Using uv (Faster)
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 3. Generate Your First Poster

```bash
# Using Python module
python -m maptoposter.cli --city "Paris" --country "France"

# Or after installation
maptoposter --city "Paris" --country "France"
```

## Project Structure

```
map-test/
├── maptoposter/              # Main package
│   ├── __init__.py          # Package exports
│   ├── poster.py            # MapPoster class (main orchestrator)
│   ├── theme.py             # Theme management
│   ├── geocoder.py          # Location geocoding
│   ├── renderer.py          # Map rendering engine
│   └── cli.py               # Command-line interface
├── tests/                    # Test suite
│   ├── __init__.py
│   └── test_maptoposter.py  # Unit tests
├── examples/                 # Usage examples
│   └── example_usage.py      # Comprehensive examples
├── pyproject.toml           # Project configuration
├── requirements.txt         # Dependencies
├── README.md                # Full documentation
├── CONTRIBUTING.md          # Contribution guidelines
├── CHANGELOG.md             # Version history
├── conftest.py              # Pytest configuration
├── pytest.ini               # Pytest settings
├── .flake8                  # Linting config
├── .gitignore               # Git ignore rules
└── LICENSE                  # MIT License
```

## Key Improvements Over v1

### 🏗️ Architecture
- **Modular Design**: Four focused classes (MapPoster, Theme, Geocoder, Renderer)
- **Separation of Concerns**: Each class handles one responsibility
- **Type Hints**: Full type annotations for better IDE support
- **Better Testing**: Comprehensive unit tests with pytest

### 📚 Code Quality
- **Documentation**: Docstrings for all public methods
- **Type Safety**: mypy compatible
- **Code Style**: Black, isort, flake8 compatible
- **Error Handling**: Better error messages and recovery

### 🚀 Development Experience
- **Pytest Suite**: Run tests with `pytest`
- **Contributing Guide**: Clear guidelines for contributors
- **Examples**: Real-world usage examples in `examples/`
- **Configuration**: Centralized config with RenderConfig and Coordinates

## Common Use Cases

### 1. Generate a Single Poster

```bash
maptoposter -c "Barcelona" -C "Spain" --theme blueprint
```

### 2. Generate Multiple Cities (Python API)

```python
from maptoposter import MapPoster

poster = MapPoster()
cities = [
    ("Paris", "France", "terracotta"),
    ("Tokyo", "Japan", "japanese_ink"),
    ("Dubai", "UAE", "midnight_blue"),
]

for city, country, theme in cities:
    poster.create_poster(city, country, theme_name=theme)
```

### 3. Custom Configuration

```python
from maptoposter import MapPoster
from maptoposter.renderer import RenderConfig

config = RenderConfig(width=16, height=20, dpi=300, distance=18000)
poster = MapPoster(renderer_config=config)
poster.create_poster("London", "UK", theme_name="noir")
```

### 4. List Available Themes

```bash
maptoposter --list-themes
```

## Development Workflow

### Run Tests

```bash
pytest
pytest --cov=maptoposter  # With coverage
```

### Format Code

```bash
black maptoposter/
isort maptoposter/
```

### Check Code Quality

```bash
flake8 maptoposter/
mypy maptoposter/
```

## Next Steps

### For Users
1. Read [README.md](README.md) for full documentation
2. Try [examples/example_usage.py](examples/example_usage.py)
3. Explore the API with `python -c "from maptoposter import MapPoster; help(MapPoster)"`

### For Contributors
1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Set up development environment
3. Create a feature branch
4. Add tests for new features
5. Submit a pull request

### For Enhancements
1. **Batch Processing**: Add CSV input for multiple cities
2. **POI Overlay**: Add landmarks, restaurants, museums
3. **Route Highlighting**: Highlight travel routes
4. **Web Dashboard**: Create UI for poster generation
5. **REST API**: Build API wrapper

## Troubleshooting

### "No module named 'maptoposter'"
```bash
# Make sure you've installed the package
pip install -e .
# Or run from project root
python -m maptoposter.cli --city "Paris" --country "France"
```

### "City not found"
- Use English city names for geocoding
- Try variations of the city name
- Use explicit coordinates with `--latitude` and `--longitude`

### Missing dependencies
```bash
pip install -r requirements.txt
```

### Memory issues with large maps
- Reduce `--distance` parameter
- Lower `--dpi` for faster preview
- Reduce `--width` and `--height`

## Support

- 📖 See [README.md](README.md) for full API documentation
- 🤝 See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- 📝 See [CHANGELOG.md](CHANGELOG.md) for version history
- 💬 Open GitHub issues for questions and bugs

## Architecture at a Glance

```
User Input (CLI/API)
        ↓
   MapPoster.create_poster()
        ↓
  ├─ Geocoder.get_coordinates()  (Get city location)
  ├─ Theme.load_theme()          (Load color scheme)
  └─ Renderer.create_map()       (Generate visual)
        ↓
   Output: PNG Poster
```

Happy mapping! 🗺️✨
