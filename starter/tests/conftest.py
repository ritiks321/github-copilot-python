"""Pytest configuration and shared fixtures."""
import pytest
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def app_context():
    """Create an application context for testing."""
    with app.app_context():
        yield app


@pytest.fixture(autouse=True)
def reset_game_state():
    """Reset the game state before each test."""
    import app as app_module
    app_module.CURRENT['puzzle'] = None
    app_module.CURRENT['solution'] = None
    yield
    # Clean up after test
    app_module.CURRENT['puzzle'] = None
    app_module.CURRENT['solution'] = None
