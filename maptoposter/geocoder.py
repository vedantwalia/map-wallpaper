"""
Geocoder module for converting city/country names to coordinates.
"""

from dataclasses import dataclass
from typing import Optional, Tuple
import requests


@dataclass
class Coordinates:
    """Represents geographic coordinates."""
    latitude: float
    longitude: float
    city: str
    country: str


class Geocoder:
    """
    Handles geocoding of city/country names to coordinates.
    
    Uses Nominatim (OpenStreetMap) as the default geocoding provider.
    """

    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
    TIMEOUT = 10

    def __init__(self, user_agent: str = "maptoposter/2.0"):
        """
        Initialize Geocoder.
        
        Args:
            user_agent: User agent for API requests
        """
        self.user_agent = user_agent
        self._cache: dict = {}

    def get_coordinates(
        self,
        city: str,
        country: str,
        lat_override: Optional[float] = None,
        lon_override: Optional[float] = None,
    ) -> Coordinates:
        """
        Get coordinates for a city and country.
        
        Args:
            city: City name
            country: Country name
            lat_override: Override latitude (optional)
            lon_override: Override longitude (optional)
            
        Returns:
            Coordinates object with latitude and longitude
            
        Raises:
            ValueError: If city/country cannot be found
        """
        # Return override coordinates if provided
        if lat_override is not None and lon_override is not None:
            return Coordinates(lat_override, lon_override, city, country)

        # Check cache
        cache_key = f"{city}_{country}".lower()
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Query Nominatim
        coords = self._query_nominatim(city, country)
        self._cache[cache_key] = coords
        return coords

    def _query_nominatim(self, city: str, country: str) -> Coordinates:
        """
        Query Nominatim API for coordinates.
        
        Args:
            city: City name
            country: Country name
            
        Returns:
            Coordinates object
            
        Raises:
            ValueError: If location not found
        """
        params = {
            "q": f"{city}, {country}",
            "format": "json",
            "limit": 1,
        }
        headers = {"User-Agent": self.user_agent}

        try:
            response = requests.get(
                self.NOMINATIM_URL,
                params=params,
                headers=headers,
                timeout=self.TIMEOUT,
            )
            response.raise_for_status()

            data = response.json()
            if not data:
                raise ValueError(f"Location not found: {city}, {country}")

            result = data[0]
            return Coordinates(
                latitude=float(result["lat"]),
                longitude=float(result["lon"]),
                city=city,
                country=country,
            )
        except requests.RequestException as e:
            raise ValueError(f"Geocoding failed: {e}")

    def clear_cache(self) -> None:
        """Clear the coordinate cache."""
        self._cache.clear()

    def __repr__(self) -> str:
        return f"Geocoder(cache_size={len(self._cache)})"
