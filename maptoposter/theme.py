"""
Theme module for managing map poster styling and appearance.
"""

import json
from pathlib import Path
from typing import Dict, Optional, Any


class Theme:
    """
    Manages theme configuration for map posters.
    
    Themes define colors and styles for different map elements like roads,
    water, parks, backgrounds, and text.
    """

    # Default theme properties
    DEFAULT_PROPERTIES = {
        "name": "default",
        "description": "Default theme",
        "bg": "#FFFFFF",
        "text": "#000000",
        "gradient_color": "#FFFFFF",
        "water": "#C0C0C0",
        "parks": "#F0F0F0",
        "road_motorway": "#0A0A0A",
        "road_primary": "#1A1A1A",
        "road_secondary": "#2A2A2A",
        "road_tertiary": "#3A3A3A",
        "road_residential": "#4A4A4A",
        "road_default": "#3A3A3A",
    }

    def __init__(self, name: str, properties: Optional[Dict[str, Any]] = None):
        """
        Initialize a Theme.
        
        Args:
            name: Theme name
            properties: Dictionary of theme properties (optional)
        """
        self.name = name
        self.properties = {**self.DEFAULT_PROPERTIES}
        if properties:
            self.properties.update(properties)

    @classmethod
    def from_json(cls, json_path: Path) -> "Theme":
        """
        Load theme from JSON file.
        
        Args:
            json_path: Path to JSON file
            
        Returns:
            Theme instance
        """
        with open(json_path, "r") as f:
            data = json.load(f)
        
        name = data.get("name", json_path.stem)
        return cls(name, data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Theme":
        """
        Create theme from dictionary.
        
        Args:
            data: Dictionary with theme properties
            
        Returns:
            Theme instance
        """
        name = data.get("name", "custom")
        return cls(name, data)

    def get(self, key: str, default: Optional[str] = None) -> str:
        """
        Get a theme property by key.
        
        Args:
            key: Property key
            default: Default value if key not found
            
        Returns:
            Property value or default
        """
        return self.properties.get(key, default)

    def __getitem__(self, key: str) -> str:
        """Allow dictionary-style access to theme properties."""
        return self.properties[key]

    def to_dict(self) -> Dict[str, Any]:
        """Return theme properties as dictionary."""
        return self.properties.copy()

    def __repr__(self) -> str:
        return f"Theme(name='{self.name}')"
