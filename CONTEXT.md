# Contexto do Projeto: Tutor IA - Cripto & Blockchain

## Visão Geral
O projeto **Tutor IA - Cripto & Blockchain** é um sistema educacional adaptativo que utiliza Inteligência Artificial (IA) para ensinar conceitos de Criptomoedas, Finanças Descentralizadas (DeFi) e Blockchain. O sistema é baseado em uma arquitetura RAG (*Retrieval-Augmented Generation*), utilizando modelos de linguagem locais para garantir privacidade total.

## Tecnologias Utilizadas
- **Backend:** FastAPI (Python)
- **Frontend:** Streamlit (Python)
- **Modelos de IA:** Ollama (LLMs locais como o Llama 3 e Nomic-embed-text para embeddings)
- **Banco Vetorial:** ChromaDB
- **Orquestração de IA:** LangChain
- **Processamento de PDFs:** PyPDF

## Arquitetura e Estrutura de Diretórios
O projeto segue os princípios da **Clean Architecture** (Arquitetura Limpa), separando as responsabilidades em camadas distintas:

- `app.py`: Interface de usuário construída com Streamlit. Ele se comunica com a API backend para enviar perguntas e exibir as respostas no chat. Permite selecionar o nível de dificuldade ("Iniciante" ou "Avançado").
- `main.py`: Ponto de entrada da API REST construída com FastAPI. Disponibiliza o endpoint `/api/v1/chat` que recebe requisições do frontend.
- `src/application/`: Contém os casos de uso (`use_cases.py`) e DTOs (`dtos.py`). O `ChatTutorUseCase` orquestra o fluxo de processamento de uma pergunta de chat.
- `src/infrastructure/`: Contém o código de infraestrutura e serviços externos.
  - `rag_service.py`: Implementa o `TutorRAGService` que configura a *chain* do LangChain (LCEL) usando o banco ChromaDB e os modelos do Ollama. Ele adapta o *prompt* baseado no nível de conhecimento do usuário.
  - `document_loaders/ingest_data.py`: Script para processar PDFs da pasta `data/`, quebrar em fragmentos (chunks) usando o `RecursiveCharacterTextSplitter`, gerar embeddings locais com o Nomic e persistir no ChromaDB (`crypto_db/`).
- `data/`: Diretório onde os PDFs e materiais educacionais devem ser inseridos.
- `crypto_db/`: Banco de dados vetorial gerado pelo ChromaDB.
- `docs/`: Documentação geral do projeto.

## Fluxo de Execução Principal (Chat RAG)
1. O usuário digita uma pergunta no Streamlit (`app.py`) e seleciona seu nível de conhecimento.
2. O Streamlit envia uma requisição POST para a API do FastAPI (`main.py`).
3. O FastAPI recebe os dados, converte via DTOs e chama o caso de uso (`ChatTutorUseCase`).
4. O caso de uso invoca o serviço de RAG (`TutorRAGService`).
5. O `TutorRAGService` busca o contexto no `ChromaDB` usando a pergunta original.
6. A pergunta, o nível do usuário e o contexto dos PDFs recuperados formam um *prompt* e são enviados para o modelo de linguagem local (`Llama 3`).
7. A resposta adaptada é devolvida para o FastAPI, que a repassa ao Streamlit para exibição no chat.

## Instalação e Execução
1. Requisitos: Python 3.10+, Ollama instalado com os modelos `llama3.1:8b` (ou similar) e `nomic-embed-text:latest`.
2. Instalar dependências: `pip install -r requirements.txt`.
3. Ingestão de dados: Colocar PDFs na pasta `data/` e rodar `python src/infrastructure/document_loaders/ingest_data.py`.
4. Rodar a API Backend: `uvicorn main:app --reload`.
5. Rodar a UI Frontend: `streamlit run app.py`.
