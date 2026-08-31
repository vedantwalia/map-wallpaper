"""
Command-line interface for MapToPoster.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .poster import MapPoster
from .renderer import RenderConfig


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        prog="maptoposter",
        description="Generate beautiful, minimalist map posters for any city in the world",
    )

    # Required arguments
    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "--city",
        "-c",
        required=True,
        help="City name (used for geocoding)",
    )
    required.add_argument(
        "--country",
        "-C",
        required=True,
        help="Country name (used for geocoding)",
    )

    # Optional arguments
    optional = parser.add_argument_group("optional arguments")
    optional.add_argument(
        "--theme",
        "-t",
        default="terracotta",
        help="Theme name (default: terracotta)",
    )
    optional.add_argument(
        "--distance",
        "-d",
        type=float,
        default=18000,
        help="Map radius in meters (default: 18000)",
    )
    optional.add_argument(
        "--width",
        "-W",
        type=float,
        default=12,
        help="Image width in inches (default: 12, max: 20)",
    )
    optional.add_argument(
        "--height",
        "-H",
        type=float,
        default=16,
        help="Image height in inches (default: 16, max: 20)",
    )
    optional.add_argument(
        "--latitude",
        "-lat",
        type=float,
        help="Override latitude center point (use with --longitude)",
    )
    optional.add_argument(
        "--longitude",
        "-long",
        type=float,
        help="Override longitude center point (use with --latitude)",
    )
    optional.add_argument(
        "--display-city",
        "-dc",
        help="Custom display name for city",
    )
    optional.add_argument(
        "--display-country",
        "-dC",
        help="Custom display name for country",
    )
    optional.add_argument(
        "--font-family",
        default="Roboto",
        help="Font family for text (default: Roboto)",
    )
    optional.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        default=Path("posters"),
        help="Output directory for posters (default: posters/)",
    )
    optional.add_argument(
        "--theme-dir",
        type=Path,
        default=Path("themes"),
        help="Theme directory (default: themes/)",
    )
    optional.add_argument(
        "--list-themes",
        action="store_true",
        help="List all available themes",
    )

    return parser


def main(argv: Optional[list] = None) -> int:
    """
    Main entry point for CLI.
    
    Args:
        argv: Command-line arguments (default: sys.argv[1:])
        
    Returns:
        Exit code
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    try:
        # Create MapPoster instance
        renderer_config = RenderConfig(
            width=args.width,
            height=args.height,
            distance=args.distance,
            font_family=args.font_family,
        )
        poster = MapPoster(
            output_dir=args.output_dir,
            theme_dir=args.theme_dir,
            renderer_config=renderer_config,
        )

        # Handle list-themes
        if args.list_themes:
            print("Available themes:")
            for theme_name in poster.list_themes():
                print(f"  - {theme_name}")
            return 0

        # Validate coordinates
        if (args.latitude is None) != (args.longitude is None):
            print(
                "Error: Both --latitude and --longitude must be provided together",
                file=sys.stderr,
            )
            return 1

        # Create poster
        print(f"Generating poster for {args.city}, {args.country}...")
        output_path = poster.create_poster(
            city=args.city,
            country=args.country,
            theme_name=args.theme,
            latitude=args.latitude,
            longitude=args.longitude,
            display_city=args.display_city,
            display_country=args.display_country,
            distance=args.distance,
            font_family=args.font_family,
        )
        print(f"✓ Poster saved to {output_path}")
        return 0

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
