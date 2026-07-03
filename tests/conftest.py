# tests/conftest.py
"""Pytest configuration and fixtures"""

import pytest
import sys
import os

# Add the parent directory to the path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db


@pytest.fixture(scope='session')
def app():
    """Create and configure a test Flask application"""
    app = create_app('testing')
    
    # Create application context
    with app.app_context():
        # Create all database tables
        db.create_all()
        yield app
        # Clean up after tests
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """A test client for the app"""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """A test runner for the app's CLI commands"""
    return app.test_cli_runner()


@pytest.fixture(autouse=True)
def reset_db(app):
    """Reset database before each test"""
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
        yield


@pytest.fixture
def auth_headers():
    """Provide authorization headers for testing"""
    return {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token'
    }


@pytest.fixture
def sample_user_data():
    """Provide sample user data for testing"""
    return {
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'test_password_123'
    }


@pytest.fixture
def sample_users():
    """Provide multiple sample users for testing"""
    return [
        {
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'john_pass_123'
        },
        {
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'password': 'jane_pass_123'
        },
        {
            'name': 'Bob Johnson',
            'email': 'bob@example.com',
            'password': 'bob_pass_123'
        }
    ]


# Pytest configuration hooks

def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


@pytest.fixture(scope='session', autouse=True)
def setup_test_environment():
    """Setup test environment"""
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['TESTING'] = 'True'
    yield


# Custom markers

def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    for item in items:
        # Add markers based on test characteristics
        if 'client' in item.fixturenames:
            item.add_marker(pytest.mark.unit)
