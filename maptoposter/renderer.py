"""
Renderer module for creating map visualizations and posters.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import osmnx as ox
import networkx as nx


@dataclass
class RenderConfig:
    """Configuration for rendering maps."""
    width: float = 12
    height: float = 16
    dpi: int = 300
    distance: float = 18000
    font_family: str = "Roboto"
    network_type: str = "drive"


class Renderer:
    """
    Handles map visualization and poster generation.
    
    Renders street networks, water features, parks, and text overlays
    using matplotlib and OSMnx.
    """

    def __init__(self, config: Optional[RenderConfig] = None):
        """
        Initialize Renderer.
        
        Args:
            config: RenderConfig object (optional)
        """
        self.config = config or RenderConfig()
        self._setup_matplotlib()

    def _setup_matplotlib(self) -> None:
        """Configure matplotlib settings."""
        if self.config.font_family.casefold() == "roboto":
            self._register_bundled_roboto()
        plt.rcParams["font.family"] = self.config.font_family
        plt.rcParams["figure.facecolor"] = "white"
        plt.rcParams["axes.facecolor"] = "white"

    @staticmethod
    def _register_bundled_roboto() -> None:
        """Make the bundled Roboto Regular, Medium, and Bold faces available."""
        fonts_dir = Path(__file__).parent / "assets" / "fonts"
        for filename in (
            "Roboto-Regular.ttf",
            "Roboto-Medium.ttf",
            "Roboto-Bold.ttf",
        ):
            font_path = fonts_dir / filename
            if font_path.is_file():
                font_manager.fontManager.addfont(str(font_path))

    def create_map(
        self,
        latitude: float,
        longitude: float,
        theme: Dict[str, str],
    ) -> Tuple[Figure, Axes]:
        """
        Create a base map figure and axes.
        
        Args:
            latitude: Center latitude
            longitude: Center longitude
            theme: Theme dictionary with colors
            
        Returns:
            Tuple of (Figure, Axes)
        """
        point = (latitude, longitude)

        # Create figure
        figsize = (self.config.width, self.config.height)
        fig, ax = plt.subplots(figsize=figsize, dpi=self.config.dpi)

        # Set background color
        fig.patch.set_facecolor(theme.get("bg", "#FFFFFF"))
        ax.set_facecolor(theme.get("bg", "#FFFFFF"))

        # Get street network
        try:
            graph = ox.graph_from_point(
                point,
                dist=self.config.distance,
                network_type=self.config.network_type,
            )
        except Exception as e:
            print(f"Warning: Could not fetch graph: {e}")
            return fig, ax

        # Plot streets
        self._plot_streets(ax, graph, theme)

        # Try to fetch and plot water and parks
        try:
            self._plot_features(ax, point, theme)
        except Exception as e:
            print(f"Warning: Could not fetch features: {e}")

        # Remove axes
        ax.axis("off")
        plt.tight_layout(pad=0)

        return fig, ax

    def _plot_streets(
        self,
        ax: Axes,
        graph: nx.MultiDiGraph,
        theme: Dict[str, str],
    ) -> None:
        """
        Plot streets from graph.
        
        Args:
            ax: Matplotlib axes
            graph: OSMnx graph
            theme: Theme dictionary
        """
        # Plot the street network using osmnx's built-in visualization
        # This automatically handles all edges with proper styling
        default_edge_color = theme.get("road_secondary", "#2A2A2A")
        
        try:
            ox.plot_graph(
                graph,
                ax=ax,
                node_size=0,
                edge_color=default_edge_color,
                edge_linewidth=0.8,
                show=False,
                close=False,
            )
        except Exception as e:
            # If ox.plot_graph fails, plot edges manually
            print(f"Warning: Could not use ox.plot_graph: {e}")
            self._plot_streets_manual(ax, graph, theme)

    def _plot_streets_manual(
        self,
        ax: Axes,
        graph: nx.MultiDiGraph,
        theme: Dict[str, str],
    ) -> None:
        """
        Manually plot streets by iterating through graph edges.
        
        Args:
            ax: Matplotlib axes
            graph: OSMnx graph
            theme: Theme dictionary
        """
        for u, v, k, data in graph.edges(keys=True, data=True):
            # Get highway type
            highway = data.get("highway", "default")
            if isinstance(highway, list):
                highway = highway[0]

            # Get color and width
            color_key = f"road_{highway}"
            color = theme.get(color_key, theme.get("road_default", "#3A3A3A"))
            width = self._get_road_width(color_key)

            # Plot edge if it has geometry
            if "geometry" in data:
                geom = data["geometry"]
                coords = list(geom.coords)
                lons = [c[0] for c in coords]
                lats = [c[1] for c in coords]
                ax.plot(lons, lats, color=color, linewidth=width, zorder=3)

    def _plot_features(
        self,
        ax: Axes,
        point: Tuple[float, float],
        theme: Dict[str, str],
    ) -> None:
        """
        Plot water and parks.
        
        Args:
            ax: Matplotlib axes
            point: (latitude, longitude) tuple
            theme: Theme dictionary
        """
        try:
            # Plot water
            water = ox.features_from_point(
                point,
                tags={"natural": "water"},
                dist=self.config.distance,
            )
            if not water.empty:
                water_color = theme.get("water", "#C0C0C0")
                water.plot(ax=ax, color=water_color, zorder=1)
        except Exception:
            pass

        try:
            # Plot parks
            parks = ox.features_from_point(
                point,
                tags={"leisure": "park"},
                dist=self.config.distance,
            )
            if not parks.empty:
                parks_color = theme.get("parks", "#F0F0F0")
                parks.plot(ax=ax, color=parks_color, zorder=2)
        except Exception:
            pass

    def _get_road_width(self, highway_type: str) -> float:
        """
        Get line width for road type.
        
        Args:
            highway_type: Highway type key
            
        Returns:
            Line width in points
        """
        widths = {
            "road_motorway": 1.2,
            "road_primary": 1.0,
            "road_secondary": 0.8,
            "road_tertiary": 0.6,
            "road_residential": 0.4,
        }
        return widths.get(highway_type, 0.4)

    def add_text_labels(
        self,
        ax: Axes,
        city: str,
        country: str,
        theme: Dict[str, str],
        display_city: Optional[str] = None,
        display_country: Optional[str] = None,
        coordinates: Optional[Tuple[float, float]] = None,
    ) -> None:
        """
        Add text labels (city, country, coordinates).
        
        Args:
            ax: Matplotlib axes
            city: City name
            country: Country name
            theme: Theme dictionary
            display_city: Custom display city name (optional)
            display_country: Custom display country name (optional)
            coordinates: (latitude, longitude) tuple (optional)
        """
        text_color = theme.get("text", "#000000")
        display_city = display_city or city
        display_country = display_country or country

        # City name
        ax.text(
            0.5,
            0.14,
            display_city.upper(),
            fontsize=32,
            weight="bold",
            ha="center",
            transform=ax.transAxes,
            color=text_color,
            zorder=11,
        )

        # Decorative line
        ax.plot(
            [0.3, 0.7],
            [0.125, 0.125],
            transform=ax.transAxes,
            color=text_color,
            linewidth=1,
            zorder=11,
        )

        # Country name
        ax.text(
            0.5,
            0.10,
            display_country.upper(),
            fontsize=14,
            ha="center",
            transform=ax.transAxes,
            color=text_color,
            zorder=11,
        )

        # Coordinates
        if coordinates:
            lat, lon = coordinates
            coord_text = f"{lat:.4f}° / {lon:.4f}°"
            ax.text(
                0.5,
                0.07,
                coord_text,
                fontsize=10,
                ha="center",
                transform=ax.transAxes,
                color=text_color,
                style="italic",
                zorder=11,
            )

    def save(self, fig: Figure, output_path: Path) -> None:
        """
        Save figure to file.
        
        Args:
            fig: Matplotlib figure
            output_path: Path to save to
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(
            output_path,
            bbox_inches="tight",
            pad_inches=0,
            dpi=self.config.dpi,
            facecolor=fig.get_facecolor(),
        )
        plt.close(fig)

    def __repr__(self) -> str:
        return (
            f"Renderer(width={self.config.width}, "
            f"height={self.config.height}, dpi={self.config.dpi})"
        )
