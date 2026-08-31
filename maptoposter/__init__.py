"""
MapToPoster: Generate beautiful, minimalist map posters for any city in the world.

A refactored, class-based implementation with modular architecture.
"""

__version__ = "2.0.0"
__author__ = "Your Name"
__license__ = "MIT"

from .poster import MapPoster
from .theme import Theme
from .geocoder import Geocoder
from .renderer import Renderer

__all__ = [
    "MapPoster",
    "Theme",
    "Geocoder",
    "Renderer",
]
