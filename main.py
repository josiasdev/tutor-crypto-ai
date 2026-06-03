from fastapi import FastAPI, Depends, HTTPException
from pydantic import ValidationError
from src.application.dtos import ChatRequest, ChatResponse
from src.application.use_cases import ChatTutorUseCase
from src.infrastructure.rag_service import TutorRAGService

# Inicializa a aplicação
app = FastAPI(
    title="API Tutor IA - Criptomoedas e Blockchain",
    description="API do agente educacional para adaptar o ensino de Web3.",
    version="1.0.0"
)

# Instância única (Singleton) do serviço para não recarregar o LLM a cada requisição
rag_service_instance = TutorRAGService()

def get_chat_use_case():
    return ChatTutorUseCase(rag_service=rag_service_instance)

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_com_tutor(
    request: ChatRequest, 
    use_case: ChatTutorUseCase = Depends(get_chat_use_case)
):
    try:
        resultado = use_case.executar(request)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok", "mensagem": "API do Tutor IA está online."}