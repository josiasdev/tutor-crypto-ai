import pytest
from pydantic import ValidationError
from src.application.dtos import ChatRequest, ChatResponse
from src.application.use_cases import ChatTutorUseCase


class TestApplicationLayer:
    """Testes unitários dos DTOs e Casos de Uso."""

    def test_chat_request_default_values(self):
        req = ChatRequest(pergunta="O que é blockchain?")
        assert req.pergunta == "O que é blockchain?"
        assert req.nivel == "Iniciante"

    def test_chat_request_custom_nivel(self):
        req = ChatRequest(pergunta="Como funciona a EVM?", nivel="Avançado")
        assert req.pergunta == "Como funciona a EVM?"
        assert req.nivel == "Avançado"

    def test_chat_request_validation_error(self):
        with pytest.raises(ValidationError):
            ChatRequest()  # pergunta é obrigatória

    def test_chat_response_creation(self):
        resp = ChatResponse(resposta="Resposta de teste")
        assert resp.resposta == "Resposta de teste"

    def test_chat_tutor_use_case_delegation(self, mocker):
        mock_rag_service = mocker.MagicMock()
        mock_rag_service.gerar_resposta.return_value = "Explicação simulada sobre Proof of Work"

        use_case = ChatTutorUseCase(rag_service=mock_rag_service)
        request = ChatRequest(pergunta="O que é PoW?", nivel="Iniciante")

        result = use_case.executar(request)

        assert isinstance(result, ChatResponse)
        assert result.resposta == "Explicação simulada sobre Proof of Work"
        mock_rag_service.gerar_resposta.assert_called_once_with(
            pergunta="O que é PoW?",
            nivel="Iniciante"
        )
