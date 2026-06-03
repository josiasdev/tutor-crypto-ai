from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    pergunta: str = Field(..., description="A pergunta do usuário sobre cripto/blockchain")
    nivel: str = Field(default="Iniciante", description="Nível de conhecimento do usuário: 'Iniciante' ou 'Avançado'")

class ChatResponse(BaseModel):
    resposta: str