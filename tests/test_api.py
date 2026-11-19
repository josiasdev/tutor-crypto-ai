from unittest.mock import MagicMock
from src.application.dtos import ChatResponse


class TestApiEndpoints:
    """Testes dos endpoints da API FastAPI (main.py)."""

    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "mensagem" in data

    def test_chat_endpoint_success(self, client, mock_use_case):
        mock_use_case.executar.return_value = ChatResponse(
            resposta="Blockchain é um livro-razão distribuído."
        )

        payload = {
            "pergunta": "O que é blockchain?",
            "nivel": "Iniciante"
        }
        response = client.post("/api/v1/chat", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["resposta"] == "Blockchain é um livro-razão distribuído."
        mock_use_case.executar.assert_called_once()

    def test_chat_endpoint_validation_error_missing_pergunta(self, client):
        payload = {"nivel": "Iniciante"}
        response = client.post("/api/v1/chat", json=payload)
        assert response.status_code == 422

    def test_chat_endpoint_internal_error(self, client, mock_use_case):
        mock_use_case.executar.side_effect = RuntimeError("Falha de conexão com LLM")

        payload = {"pergunta": "Qualquer pergunta"}
        response = client.post("/api/v1/chat", json=payload)

        assert response.status_code == 500
        data = response.json()
        assert "Falha de conexão com LLM" in data["detail"]
