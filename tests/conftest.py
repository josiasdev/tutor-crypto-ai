import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from main import app, get_chat_use_case
from src.application.dtos import ChatResponse
from src.application.use_cases import ChatTutorUseCase


@pytest.fixture
def mock_use_case():
    """Mock do caso de uso ChatTutorUseCase para isolar a API REST."""
    use_case = MagicMock(spec=ChatTutorUseCase)
    return use_case


@pytest.fixture
def client(mock_use_case):
    """Cliente de teste do FastAPI com injeção de dependência sobreposta."""
    app.dependency_overrides[get_chat_use_case] = lambda: mock_use_case
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
