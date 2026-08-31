# MapToPoster

Generate beautiful, minimalist map posters for any city in the world.

This is a refactored, class-based version of MapToPoster with modular architecture for better maintainability, testability, and extensibility.

## Key Features

✨ **Modular Architecture**
- `MapPoster`: Main orchestrator class
- `Theme`: Theme management system
- `Geocoder`: Location-to-coordinates conversion
- `Renderer`: Map visualization and rendering

🗺️ **Powerful Mapping**
- Generate maps for any city worldwide
- Customizable zoom distance
- Street network visualization
- Water and parks overlay
- Multiple pre-built themes

🎨 **17 Built-in Themes**
- terracotta, noir, blueprint, sunset
- midnight_blue, neon_cyberpunk, forest, ocean
- japanese_ink, emerald, pastel_dream, warm_beige
- And more...

📊 **High-Quality Output**
- 300 DPI by default
- Configurable dimensions (up to 20x20 inches)
- PNG export ready for print
- Customizable font families

🌍 **Multilingual Support**
- Display city names in any language
- Custom font support for non-Latin scripts
- Google Fonts integration ready

## Installation

### Quick Start (with uv - Recommended)

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone https://github.com/yourusername/maptoposter.git
cd maptoposter
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### Alternative (pip + venv)

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Usage

### As a Command-Line Tool

```bash
# Basic usage
python -m maptoposter.cli --city "Paris" --country "France"

# With theme
python -m maptoposter.cli -c "Tokyo" -C "Japan" --theme japanese_ink

# List available themes
python -m maptoposter.cli --list-themes

# Custom display names (multilingual)
python -m maptoposter.cli -c "Tokyo" -C "Japan" \
  --display-city "東京" \
  --display-country "日本" \
  --font-family "Noto Sans JP"
```

### As a Python Package

```python
from maptoposter import MapPoster
from maptoposter.renderer import RenderConfig

# Create poster generator
config = RenderConfig(width=12, height=16, dpi=300)
poster = MapPoster(renderer_config=config)

# Generate a poster
output_path = poster.create_poster(
    city="Paris",
    country="France",
    theme_name="terracotta",
    distance=15000,
)

print(f"Poster saved to {output_path}")
```

### Advanced Usage

```python
from maptoposter import MapPoster, Geocoder
from maptoposter.renderer import RenderConfig

# Custom geocoder with coordinate caching
geocoder = Geocoder(user_agent="my-app/1.0")

# Configure rendering
config = RenderConfig(
    width=16,
    height=20,
    dpi=300,
    distance=20000,
    font_family="Roboto",
)

# Create poster with custom config
poster = MapPoster(
    output_dir="./my_posters",
    theme_dir="./my_themes",
    geocoder=geocoder,
    renderer_config=config,
)

# Generate with custom coordinates
output = poster.create_poster(
    city="New York",
    country="USA",
    theme_name="noir",
    latitude=40.7128,
    longitude=-74.0060,
    display_city="NEW YORK",
)
```

## Command-Line Options

### Required Arguments

| Option | Short | Description |
|--------|-------|-------------|
| `--city` | `-c` | City name (used for geocoding) |
| `--country` | `-C` | Country name (used for geocoding) |

### Optional Arguments

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--theme` | `-t` | terracotta | Theme name |
| `--distance` | `-d` | 18000 | Map radius in meters |
| `--width` | `-W` | 12 | Image width in inches (max: 20) |
| `--height` | `-H` | 16 | Image height in inches (max: 20) |
| `--latitude` | `-lat` | - | Override latitude (use with --longitude) |
| `--longitude` | `-long` | - | Override longitude (use with --latitude) |
| `--display-city` | `-dc` | - | Custom display name for city |
| `--display-country` | `-dC` | - | Custom display name for country |
| `--font-family` | - | Roboto | Font family for text |
| `--output-dir` | `-o` | posters/ | Output directory |
| `--theme-dir` | - | themes/ | Theme directory |
| `--list-themes` | - | - | List all available themes |

## Architecture

### Class Overview

#### MapPoster
Main orchestrator class that coordinates all components.

```python
poster = MapPoster(
    output_dir=Path("posters"),
    theme_dir=Path("themes"),
    geocoder=Geocoder(),
    renderer_config=RenderConfig(),
)

# Create a poster
output_path = poster.create_poster(
    city="Paris",
    country="France",
    theme_name="blueprint",
)
```

#### Geocoder
Converts city/country names to geographic coordinates using Nominatim API.

```python
from maptoposter import Geocoder

geocoder = Geocoder()
coords = geocoder.get_coordinates("Paris", "France")
print(f"Latitude: {coords.latitude}, Longitude: {coords.longitude}")
```

#### Theme
Manages theme properties and styling.

```python
from maptoposter import Theme

# Load from JSON
theme = Theme.from_json(Path("themes/custom.json"))

# Create from dict
theme = Theme.from_dict({
    "name": "my_theme",
    "bg": "#FFFFFF",
    "text": "#000000",
    # ... more properties
})

# Access properties
color = theme["road_motorway"]
color = theme.get("water", "#C0C0C0")
```

#### Renderer
Handles map visualization and poster generation.

```python
from maptoposter.renderer import Renderer, RenderConfig

config = RenderConfig(width=12, height=16, dpi=300)
renderer = Renderer(config)

fig, ax = renderer.create_map(48.8566, 2.3522, theme_dict)
renderer.add_text_labels(ax, "Paris", "France", theme_dict)
renderer.save(fig, Path("posters/paris.png"))
```

### Module Structure

```
maptoposter/
├── __init__.py          # Package exports
├── poster.py            # Main MapPoster class
├── theme.py             # Theme management
├── geocoder.py          # Geocoding service
├── renderer.py          # Map rendering engine
├── cli.py               # Command-line interface
└── utils.py             # Utility functions (future)
```

## Examples

### Generate a Simple Poster

```bash
python -m maptoposter.cli -c "Barcelona" -C "Spain"
```

### Create Multiple Posters

```python
cities = [
    ("Paris", "France", "terracotta"),
    ("Tokyo", "Japan", "japanese_ink"),
    ("Dubai", "UAE", "midnight_blue"),
]

poster = MapPoster()
for city, country, theme in cities:
    output = poster.create_poster(city, country, theme_name=theme)
    print(f"Generated: {output}")
```

### Custom Theme Creation

Create a JSON file in the `themes/` directory:

```json
{
  "name": "my_custom_theme",
  "description": "My custom map theme",
  "bg": "#1a1a1a",
  "text": "#ffffff",
  "gradient_color": "#2a2a2a",
  "water": "#2e5c8a",
  "parks": "#3d5a3d",
  "road_motorway": "#ffcc00",
  "road_primary": "#ffaa00",
  "road_secondary": "#ff8800",
  "road_tertiary": "#ff6600",
  "road_residential": "#ff4400",
  "road_default": "#ff4400"
}
```

## Resolution Guide (300 DPI)

| Use Case | Dimensions | Width × Height |
|----------|-----------|----------------|
| Instagram Post | 1080 × 1080 | 3.6 × 3.6" |
| Mobile Wallpaper | 1080 × 1920 | 3.6 × 6.4" |
| HD Wallpaper | 1920 × 1080 | 6.4 × 3.6" |
| 4K Wallpaper | 3840 × 2160 | 12.8 × 7.2" |
| A4 Print | 2480 × 3508 | 8.3 × 11.7" |

## Distance Guide

| Distance | Best For |
|----------|----------|
| 4,000-6,000m | Small/dense cities (Venice, Amsterdam center) |
| 8,000-12,000m | Medium cities, focused downtown (Paris, Barcelona) |
| 15,000-20,000m | Large metros, full city view (Tokyo, Mumbai) |

## Development

### Running Tests

```bash
pytest
pytest --cov=maptoposter
```

### Code Quality

```bash
black maptoposter/
isort maptoposter/
flake8 maptoposter/
mypy maptoposter/
```

### Type Hints

The project uses Python type hints throughout. For development, ensure your IDE is configured for type checking.

## Future Enhancements

- [ ] Batch CSV processing for multiple cities
- [ ] POI (Points of Interest) overlay
- [ ] Route highlighting and paths
- [ ] SVG/PDF vector export
- [ ] REST API wrapper
- [ ] Web dashboard interface
- [ ] Plugin system for custom layers
- [ ] Color palette generation from images
- [ ] Print-ready frame mockups
- [ ] Social media automation

## Dependencies

- **matplotlib**: Visualization and rendering
- **osmnx**: OpenStreetMap data fetching
- **networkx**: Graph processing
- **geopandas**: Geospatial data handling
- **shapely**: Geometric operations
- **requests**: HTTP requests for geocoding

## License

MIT License - see LICENSE file for details

## Credits

This is a refactored, class-based version of the original MapToPoster project.

### Original Contributors
- [@originalankur](https://github.com/originalankur)
- And many community contributors

### Refactored By
Your Name

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request
4. Include tests for new functionality

## Troubleshooting

### "City not found" Error

Ensure the city and country names are in English. For display in other languages, use the `--display-city` and `--display-country` flags.

### Slow Geocoding

The geocoder caches results. If you're generating many posters, subsequent runs will be faster.

### Memory Issues

Large distance values (>20km) consume more memory. Try:
- Reducing `--distance`
- Reducing `--width` and `--height`
- Setting lower `--dpi`

### Missing OSM Data

Some cities may have incomplete OpenStreetMap data. Try:
- Adjusting the zoom distance
- Using explicit `--latitude` and `--longitude` coordinates

## Support

For issues, questions, or suggestions, please:
- Open an issue on GitHub
- Check existing discussions
- Review the architecture documentation

## See Also

- [Original MapToPoster](https://github.com/originalankur/maptoposter)
- [OSMnx Documentation](https://osmnx.readthedocs.io/)
- [Nominatim](https://nominatim.org/)
- [Matplotlib](https://matplotlib.org/)
