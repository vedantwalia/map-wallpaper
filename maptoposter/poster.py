"""
Main MapPoster class - orchestrates all components.
"""

from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from .theme import Theme
from .geocoder import Geocoder, Coordinates
from .renderer import Renderer, RenderConfig


class MapPoster:
    """
    Main class for generating map posters.
    
    Orchestrates geocoding, theme management, and rendering to create
    beautiful minimalist map posters for cities worldwide.
    """

    DEFAULT_OUTPUT_DIR = Path("posters")
    DEFAULT_THEME_DIR = Path("themes")

    def __init__(
        self,
        output_dir: Optional[Path] = None,
        theme_dir: Optional[Path] = None,
        geocoder: Optional[Geocoder] = None,
        renderer_config: Optional[RenderConfig] = None,
    ):
        """
        Initialize MapPoster.
        
        Args:
            output_dir: Directory for output posters
            theme_dir: Directory containing theme files
            geocoder: Geocoder instance (optional)
            renderer_config: RenderConfig for rendering (optional)
        """
        self.output_dir = Path(output_dir or self.DEFAULT_OUTPUT_DIR)
        self.theme_dir = Path(theme_dir or self.DEFAULT_THEME_DIR)
        self.geocoder = geocoder or Geocoder()
        self.renderer_config = renderer_config or RenderConfig()
        self._theme_cache: Dict[str, Theme] = {}

    def create_poster(
        self,
        city: str,
        country: str,
        theme_name: str = "terracotta",
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        display_city: Optional[str] = None,
        display_country: Optional[str] = None,
        distance: Optional[float] = None,
        font_family: Optional[str] = None,
    ) -> Path:
        """
        Create a map poster for a city.
        
        Args:
            city: City name
            country: Country name
            theme_name: Theme name (default: "terracotta")
            latitude: Override latitude (optional)
            longitude: Override longitude (optional)
            display_city: Custom display name for city (optional)
            display_country: Custom display name for country (optional)
            distance: Map radius in meters (optional)
            font_family: Font family for text (optional)
            
        Returns:
            Path to generated poster
            
        Raises:
            ValueError: If city/country not found or rendering fails
        """
        # Get coordinates
        coords = self.geocoder.get_coordinates(city, country, latitude, longitude)

        # Load theme
        theme = self.load_theme(theme_name)

        # Configure renderer
        config = self.renderer_config
        if distance:
            config.distance = distance
        if font_family:
            config.font_family = font_family

        # Create renderer
        renderer = Renderer(config)

        # Create map
        fig, ax = renderer.create_map(coords.latitude, coords.longitude, theme.to_dict())

        # Add text labels
        renderer.add_text_labels(
            ax,
            city,
            country,
            theme.to_dict(),
            display_city=display_city,
            display_country=display_country,
            coordinates=(coords.latitude, coords.longitude),
        )

        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{city.lower()}_{theme_name}_{timestamp}.png"
        output_path = self.output_dir / output_filename

        # Save poster
        renderer.save(fig, output_path)

        return output_path

    def load_theme(self, theme_name: str) -> Theme:
        """
        Load a theme by name.
        
        Args:
            theme_name: Name of the theme
            
        Returns:
            Theme object
            
        Raises:
            ValueError: If theme not found
        """
        # Check cache
        if theme_name in self._theme_cache:
            return self._theme_cache[theme_name]

        # Try to load from JSON file
        theme_path = self.theme_dir / f"{theme_name}.json"
        if theme_path.exists():
            theme = Theme.from_json(theme_path)
            self._theme_cache[theme_name] = theme
            return theme

        # Try built-in theme
        builtin_theme = self._get_builtin_theme(theme_name)
        if builtin_theme:
            theme = Theme.from_dict(builtin_theme)
            self._theme_cache[theme_name] = theme
            return theme

        raise ValueError(f"Theme not found: {theme_name}")

    def _get_builtin_theme(self, theme_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a built-in theme by name.
        
        Args:
            theme_name: Name of the theme
            
        Returns:
            Theme dictionary or None
        """
        themes = self._get_builtin_themes_dict()
        return themes.get(theme_name)

    def _get_builtin_themes_dict(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all built-in themes.
        
        Returns:
            Dictionary of all built-in themes
        """
        return {
            "terracotta": {
                "name": "terracotta",
                "description": "Mediterranean warmth",
                "bg": "#D4A574",
                "text": "#2C1810",
                "water": "#8B7355",
                "parks": "#A0826D",
                "road_motorway": "#3E2723",
                "road_primary": "#5D4037",
                "road_secondary": "#795548",
                "road_tertiary": "#A1887F",
                "road_residential": "#BCAAA4",
            },
            "noir": {
                "name": "noir",
                "description": "Pure black background, white roads",
                "bg": "#000000",
                "text": "#FFFFFF",
                "water": "#1A1A1A",
                "parks": "#2A2A2A",
                "road_motorway": "#FFFFFF",
                "road_primary": "#E0E0E0",
                "road_secondary": "#BDBDBD",
                "road_tertiary": "#9E9E9E",
                "road_residential": "#757575",
            },
            "blueprint": {
                "name": "blueprint",
                "description": "Architectural blueprint aesthetic",
                "bg": "#003DA5",
                "text": "#00D9FF",
                "water": "#00A8E8",
                "parks": "#0066CC",
                "road_motorway": "#00D9FF",
                "road_primary": "#00C5FF",
                "road_secondary": "#0099FF",
                "road_tertiary": "#0077FF",
                "road_residential": "#0055DD",
            },
            "sunset": {
                "name": "sunset",
                "description": "Warm oranges and pinks",
                "bg": "#FF6B35",
                "text": "#FFF3B0",
                "water": "#E09F3E",
                "parks": "#D62828",
                "road_motorway": "#FFFFFF",
                "road_primary": "#FFF8DC",
                "road_secondary": "#FFE5B4",
                "road_tertiary": "#FFDAB9",
                "road_residential": "#FFD7A8",
            },
        }

    def list_themes(self) -> list:
        """
        List all available themes.
        
        Returns:
            List of theme names
        """
        themes = set()

        # Add built-in themes
        themes.update(self._get_builtin_themes_dict().keys())

        # Add themes from directory
        if self.theme_dir.exists():
            for json_file in self.theme_dir.glob("*.json"):
                themes.add(json_file.stem)

        return sorted(themes)

    def clear_cache(self) -> None:
        """Clear theme and geocoder caches."""
        self._theme_cache.clear()
        self.geocoder.clear_cache()

    def __repr__(self) -> str:
        return (
            f"MapPoster(output_dir='{self.output_dir}', "
            f"theme_dir='{self.theme_dir}')"
        )
