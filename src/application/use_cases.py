from src.application.dtos import ChatRequest, ChatResponse
from src.infrastructure.rag_service import TutorRAGService

class ChatTutorUseCase:
    def __init__(self, rag_service: TutorRAGService):
        self.rag_service = rag_service

    def executar(self, request: ChatRequest) -> ChatResponse:
        # Aqui poderíamos adicionar lógicas extras, como salvar log no banco,
        # validar se a pergunta contém palavras proibidas, etc.
        resposta_texto = self.rag_service.gerar_resposta(
            pergunta=request.pergunta,
            nivel=request.nivel
        )
        return ChatResponse(resposta=resposta_texto)