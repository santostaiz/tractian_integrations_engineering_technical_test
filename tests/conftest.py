import pytest
from src.tracOS.repository import TracOSRepository


@pytest.fixture
def repo():
    return TracOSRepository()