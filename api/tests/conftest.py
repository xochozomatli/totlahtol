from totlahtol import create_app
import pytest

def test_simple():
    assert True

@pytest.fixture
def app():
    app = create_app()
    return app
