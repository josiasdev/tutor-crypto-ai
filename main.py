from fastapi import FastAPI, Depends, HTTPException
from src.application.dtos import ChatRequest, ChatResponse
from src.application.use_cases import ChatTutorUseCase
from src.infrastructure.rag_service import TutorRAGService

SWAGGER_DESCRIPTION = """
API de inferência e tutoria personalizada para o ensino de Criptomoedas e Tecnologia Blockchain.

Projeto acadêmico desenvolvido na Universidade Federal do Ceará (UFC - Campus Quixadá).
O sistema emprega Agentes de Inteligência Artificial com Recuperação Aumentada de Geração (RAG)
e modelos locais executados via Ollama, garantindo soberania de dados e ancoragem documental estrita.

Contatos e Perfis Profissionais:
- LinkedIn: https://www.linkedin.com/in/josias-batista/
- Portfólio: https://josias-batista-portfolio.vercel.app
- GitHub: https://github.com/josiasdev
"""

tags_metadata = [
    {
        "name": "Tutoria Cognitiva",
        "description": "Endpoints para interação e geração de respostas adaptativas via RAG.",
    },
    {
        "name": "Monitoramento",
        "description": "Verificação de disponibilidade e integridade do serviço.",
    },
]

# Inicializa a aplicação com metadados estruturados
app = FastAPI(
    title="Tutor Crypto AI - API Educacional",
    description=SWAGGER_DESCRIPTION,
    version="1.0.0",
    openapi_tags=tags_metadata,
    contact={
        "name": "Josias Batista",
        "url": "https://josias-batista-portfolio.vercel.app",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Instância única (Singleton) do serviço para não recarregar o LLM a cada requisição
rag_service_instance = TutorRAGService()


def get_chat_use_case():
    return ChatTutorUseCase(rag_service=rag_service_instance)


@app.post(
    "/api/v1/chat",
    response_model=ChatResponse,
    tags=["Tutoria Cognitiva"],
    summary="Processa pergunta educacional e gera resposta adaptada ao perfil do estudante",
    response_description="Resposta didática formatada com base estrita no corpus documental indexado.",
)
async def chat_com_tutor(
    request: ChatRequest,
    use_case: ChatTutorUseCase = Depends(get_chat_use_case),
):
    """
    Submete uma dúvida conceitual ou técnica sobre Blockchain e Criptomoedas.

    Parâmetros:
    - pergunta: Dúvida formulada pelo discente.
    - nivel: Perfil pedagógico do usuário ('Iniciante' para analogias e explicações graduais; 'Avançado' para terminologia formal, arquitetura e componentes criptográficos).
    """
    try:
        resultado = use_case.executar(request)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/health",
    tags=["Monitoramento"],
    summary="Verifica o status operacional da API",
    response_description="Confirmação de integridade operacional do serviço REST.",
)
def health_check():
    """Retorna o estado operacional e conectividade do backend."""
    return {"status": "ok", "mensagem": "API do Tutor IA está online."}
