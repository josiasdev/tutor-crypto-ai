# Contexto do Projeto: Agente de IA como Tutor Personalizado de Criptomoedas e Blockchain

## Visão Geral
O projeto **Tutor Crypto AI** é um Sistema Tutor Inteligente (ITS) baseado em Agentes de Inteligência Artificial e Recuperação Aumentada de Geração (RAG), projetado para apoiar o ensino-aprendizagem de **Criptomoedas** e **tecnologia Blockchain**. A arquitetura executa modelos de linguagem localmente via Ollama para garantir privacidade de dados, autonomia operacional e controle rigoroso contra alucinações factuais.

## Stack Tecnológica
- **Backend:** FastAPI (Python 3.10+) com validação via Pydantic e controle de sessão JWT
- **Frontend:** Streamlit (Python) com gerenciamento de estado de sessão e histórico de interações
- **Inferência Local:** Ollama executando Llama 3 / Llama 3.1 (8B) e `nomic-embed-text`
- **Banco Vetorial:** ChromaDB (persistência local em `crypto_db/`)
- **Orquestração Cognitiva:** LangChain e LangChain Expression Language (LCEL)
- **Processamento Documental:** PyPDF (`PyPDFDirectoryLoader` e `RecursiveCharacterTextSplitter`)

## Arquitetura e Responsabilidades das Camadas
O sistema adota princípios de **Clean Architecture**, dividindo o código em quatro camadas principais:

- `app.py` (Camada de Apresentação Web): Interface desenvolvida em Streamlit. Permite ao estudante selecionar o perfil de proficiência (`Iniciante` ou `Avançado`), visualizar o histórico persistido da sessão atual e submeter dúvidas sobre Criptomoedas e Blockchain.
- `main.py` e `src/presentation/` (Camada de Serviços REST): API FastAPI que expõe os endpoints de autenticação de sessão (`/api/v1/auth`) e conversação (`/api/v1/chat`), realizando validação de payload e isolamento de contexto por usuário via middleware JWT.
- `src/application/` (Camada de Aplicação): Contém os DTOs (`dtos.py`) e os casos de uso (`use_cases.py`). O `ChatTutorUseCase` coordena o recebimento da consulta, o perfil do estudante e a chamada ao serviço cognitivo.
- `src/infrastructure/` (Camada de Infraestrutura e RAG):
  - `rag_service.py`: Implementa o `TutorRAGService` utilizando LCEL (`RunnablePassthrough`, `RunnableLambda`, `ChatPromptTemplate` e `StrOutputParser`). Configura a busca por similaridade de cosseno (`Top-k = 3`) no ChromaDB e injeta diretrizes pedagógicas dinâmicas no `system prompt`, restringindo a resposta exclusivamente aos trechos recuperados.
  - `document_loaders/ingest_data.py`: Lê recursivamente os PDFs em Português do Brasil (pt-BR) armazenados em `data/01_blockchain/` e `data/02_criptomoedas/`, aplica fragmentação com sobreposição (`chunk overlap`), gera embeddings com Nomic e grava os vetores no ChromaDB.
- `docs/avaliacao/` (Instrumentos da Fase 2 - TCC 2): Contém o questionário estruturado em Escala Likert de 5 pontos aplicado aos discentes voluntários da UFC Campus Quixadá, cobrindo usabilidade da interface, clareza didática, confiabilidade técnica percebida e utilidade pedagógica.
- `tests/` (Verificação Funcional): Suíte de casos de teste (CT-01 a CT-06) que valida a recuperação semântica e a adaptação discursiva nos dois eixos temáticos, além da recusa explícita a perguntas fora do escopo documental.

## Ciclo Percepção-Decisão-Ação do Agente
1. **Percepção:** O estudante envia uma pergunta e seleciona seu nível de conhecimento (`Iniciante` ou `Avançado`) no Streamlit (`app.py`).
2. **Roteamento e Sessão:** O Streamlit envia uma requisição POST autenticada por token JWT para o FastAPI (`main.py`), que valida os dados e aciona o `ChatTutorUseCase`.
3. **Recuperação Contextual:** O `TutorRAGService` converte a pergunta em vetor denso e recupera os 3 trechos mais relevantes (`k = 3`) da base curada no `ChromaDB`.
4. **Adaptação Pedagógica:** A cadeia LCEL compõe o `system prompt` conforme o perfil do estudante (analogias cotidianas para Iniciante; definições formais de criptografia, consenso e execução determinística para Avançado) e anexa os trechos recuperados.
5. **Geração Ancorada:** O modelo local Llama 3 processa o prompt e gera a resposta restrita ao contexto documental, recusando extrapolações especulativas ou temas ausentes da base.
6. **Entrega:** A resposta formatada retorna via FastAPI ao Streamlit, atualizando o histórico da sessão do estudante.

## Comandos Rápidos de Operação
1. **Ingestão de Dados:** `python src/infrastructure/document_loaders/ingest_data.py`
2. **Execução da API:** `uvicorn main:app --reload`
3. **Execução da Interface:** `streamlit run app.py`
4. **Execução dos Testes:** `pytest tests/`