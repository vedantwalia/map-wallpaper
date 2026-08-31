"""Tests for maptoposter package."""

import pytest
from pathlib import Path
from maptoposter import Theme, Geocoder, Renderer, MapPoster
from maptoposter.renderer import RenderConfig
import maptoposter.renderer as renderer_module


@pytest.fixture
def theme():
    """Create a test theme."""
    return Theme("test", {
        "bg": "#FFFFFF",
        "text": "#000000",
        "water": "#0000FF",
        "parks": "#00FF00",
    })


@pytest.fixture
def geocoder():
    """Create a geocoder instance."""
    return Geocoder()


@pytest.fixture
def render_config():
    """Create a render config for testing."""
    return RenderConfig(width=8, height=10, dpi=100, distance=10000)


class TestTheme:
    """Test Theme class."""
    
    def test_theme_creation(self, theme):
        """Test creating a theme."""
        assert theme.name == "test"
        assert theme["bg"] == "#FFFFFF"
        assert theme.get("text") == "#000000"
    
    def test_theme_from_dict(self):
        """Test creating theme from dict."""
        data = {"name": "custom", "bg": "#000000"}
        theme = Theme.from_dict(data)
        assert theme.name == "custom"
        assert theme["bg"] == "#000000"
    
    def test_theme_default_values(self, theme):
        """Test theme has default values."""
        # Should have default properties even if not specified
        assert "road_motorway" in theme.to_dict()


class TestGeocoder:
    """Test Geocoder class."""
    
    def test_geocoder_creation(self, geocoder):
        """Test creating a geocoder."""
        assert geocoder is not None
        assert len(geocoder._cache) == 0
    
    def test_geocoder_coordinate_override(self, geocoder):
        """Test coordinate override."""
        coords = geocoder.get_coordinates(
            "Test", "City",
            lat_override=48.8566,
            lon_override=2.3522
        )
        assert coords.latitude == 48.8566
        assert coords.longitude == 2.3522
    
    def test_geocoder_cache(self, geocoder):
        """Test geocoder caching."""
        # Use coordinate overrides - they won't use cache
        # but subsequent calls will return same result
        coords1 = geocoder.get_coordinates(
            "Test City", "Test Country",
            lat_override=48.8566,
            lon_override=2.3522
        )
        coords2 = geocoder.get_coordinates(
            "Test City", "Test Country",
            lat_override=48.8566,
            lon_override=2.3522
        )
        # Should return consistent results
        assert coords1.latitude == coords2.latitude
        assert coords1.longitude == coords2.longitude
        # With overrides, cache won't be used
        assert len(geocoder._cache) == 0
        
        # Test cache clear functionality
        geocoder.clear_cache()
        assert len(geocoder._cache) == 0


class TestRenderer:
    """Test Renderer class."""
    
    def test_renderer_creation(self, render_config):
        """Test creating a renderer."""
        renderer = Renderer(render_config)
        assert renderer.config == render_config
    
    def test_renderer_default_config(self):
        """Test renderer with default config."""
        renderer = Renderer()
        assert renderer.config.dpi == 300
        assert renderer.config.width == 12

    def test_default_renderer_registers_bundled_roboto(self, monkeypatch):
        """The default typeface should be available without a system font install."""
        registered_fonts = []
        monkeypatch.setattr(
            renderer_module.font_manager.fontManager,
            "addfont",
            registered_fonts.append,
        )

        Renderer()

        assert registered_fonts == [
            str(Path(renderer_module.__file__).parent / "assets" / "fonts" / filename)
            for filename in (
                "Roboto-Regular.ttf",
                "Roboto-Medium.ttf",
                "Roboto-Bold.ttf",
            )
        ]

    def test_add_text_labels_is_supported_by_matplotlib(self, render_config, theme):
        """Text labels should not rely on unsupported Text properties."""
        renderer = Renderer(render_config)
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        try:
            renderer.add_text_labels(
                ax,
                "Paris",
                "France",
                theme.to_dict(),
                coordinates=(48.8566, 2.3522),
            )
            assert [text.get_text() for text in ax.texts] == [
                "PARIS",
                "FRANCE",
                "48.8566° / 2.3522°",
            ]
        finally:
            plt.close(fig)


class TestMapPoster:
    """Test MapPoster class."""
    
    def test_maptoposter_creation(self):
        """Test creating a MapPoster."""
        poster = MapPoster()
        assert poster is not None
        assert poster.output_dir == Path("posters")
    
    def test_load_builtin_theme(self):
        """Test loading built-in themes."""
        poster = MapPoster()
        theme = poster.load_theme("terracotta")
        assert theme.name == "terracotta"
        assert "bg" in theme.to_dict()
    
    def test_list_themes(self):
        """Test listing available themes."""
        poster = MapPoster()
        themes = poster.list_themes()
        assert len(themes) > 0
        assert "terracotta" in themes or "noir" in themes


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
