#!/usr/bin/env python
"""
Example script demonstrating MapToPoster usage.

Run this with: python examples/example_usage.py
"""

from pathlib import Path
from maptoposter import MapPoster, Geocoder
from maptoposter.renderer import RenderConfig


def example_basic():
    """Example 1: Basic usage with defaults."""
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    poster = MapPoster()
    
    # Generate a simple poster
    output = poster.create_poster(
        city="Paris",
        country="France",
        theme_name="terracotta",
    )
    print(f"✓ Generated: {output}\n")


def example_custom_config():
    """Example 2: Custom rendering configuration."""
    print("=" * 60)
    print("Example 2: Custom Rendering Configuration")
    print("=" * 60)
    
    # Configure rendering options
    config = RenderConfig(
        width=16,
        height=20,
        dpi=300,
        distance=15000,
        font_family="Roboto",
    )
    
    poster = MapPoster(
        output_dir=Path("output/posters"),
        renderer_config=config,
    )
    
    output = poster.create_poster(
        city="Tokyo",
        country="Japan",
        theme_name="japanese_ink",
        distance=20000,
    )
    print(f"✓ Generated: {output}\n")


def example_multilingual():
    """Example 3: Multilingual support."""
    print("=" * 60)
    print("Example 3: Multilingual Support")
    print("=" * 60)
    
    poster = MapPoster()
    
    # Generate poster with Japanese characters
    output = poster.create_poster(
        city="Tokyo",
        country="Japan",
        theme_name="japanese_ink",
        display_city="東京",
        display_country="日本",
        font_family="Noto Sans JP",
    )
    print(f"✓ Generated Japanese poster: {output}")
    
    # Arabic
    output = poster.create_poster(
        city="Dubai",
        country="UAE",
        theme_name="midnight_blue",
        display_city="دبي",
        display_country="الإمارات",
        font_family="Cairo",
    )
    print(f"✓ Generated Arabic poster: {output}\n")


def example_batch():
    """Example 4: Batch generation of multiple posters."""
    print("=" * 60)
    print("Example 4: Batch Generation")
    print("=" * 60)
    
    cities = [
        ("Paris", "France", "terracotta"),
        ("Venice", "Italy", "blueprint"),
        ("Barcelona", "Spain", "warm_beige"),
        ("Tokyo", "Japan", "japanese_ink"),
        ("Dubai", "UAE", "midnight_blue"),
        ("Sydney", "Australia", "ocean"),
    ]
    
    poster = MapPoster(output_dir=Path("output/batch"))
    
    for city, country, theme in cities:
        try:
            output = poster.create_poster(
                city=city,
                country=country,
                theme_name=theme,
            )
            print(f"✓ {city:15} ({theme:20}) -> {output.name}")
        except Exception as e:
            print(f"✗ {city:15} Failed: {e}")
    
    print()


def example_coordinates():
    """Example 5: Using explicit coordinates."""
    print("=" * 60)
    print("Example 5: Explicit Coordinates")
    print("=" * 60)
    
    poster = MapPoster()
    
    # NYC coordinates (can be found from geocoding or maps)
    output = poster.create_poster(
        city="New York",
        country="USA",
        latitude=40.7128,
        longitude=-74.0060,
        theme_name="noir",
        distance=12000,
    )
    print(f"✓ Generated NYC poster: {output}\n")


def example_list_themes():
    """Example 6: List available themes."""
    print("=" * 60)
    print("Example 6: Available Themes")
    print("=" * 60)
    
    poster = MapPoster()
    
    themes = poster.list_themes()
    print(f"Total themes available: {len(themes)}\n")
    print("Themes:")
    for theme in sorted(themes):
        print(f"  - {theme}")
    print()


def example_custom_output():
    """Example 7: Custom output directory."""
    print("=" * 60)
    print("Example 7: Custom Output Directory")
    print("=" * 60)
    
    custom_dir = Path("my_posters")
    poster = MapPoster(output_dir=custom_dir)
    
    output = poster.create_poster(
        city="Amsterdam",
        country="Netherlands",
        theme_name="blueprint",
    )
    print(f"✓ Generated in custom directory: {output}\n")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("MapToPoster v2.0 - Usage Examples")
    print("=" * 60 + "\n")
    
    try:
        # Run examples
        example_basic()
        example_custom_config()
        example_multilingual()
        example_batch()
        example_coordinates()
        example_list_themes()
        example_custom_output()
        
        print("=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        print("\nMake sure you have installed dependencies:")
        print("  pip install -r requirements.txt")


if __name__ == "__main__":
    main()
