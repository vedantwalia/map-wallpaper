"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path
import sys

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary output directory for tests."""
    return tmp_path / "output"


@pytest.fixture
def temp_theme_dir(tmp_path):
    """Create a temporary theme directory for tests."""
    return tmp_path / "themes"
