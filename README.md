# 🪙 Agente de IA: Tutor Personalizado de Web3 & Blockchain

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111%2B-009688)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B)
![LangChain](https://img.shields.io/badge/LangChain-0.2%2B-green)

Este projeto apresenta o desenvolvimento de um Agente de Inteligência Artificial para atuar como tutor educacional iterativo no ensino de Criptomoedas, Finanças Descentralizadas (DeFi) e tecnologia Blockchain. 

O sistema adapta dinamicamente a sua didática (do nível iniciante ao avançado) utilizando técnicas de RAG (*Retrieval-Augmented Generation*) com modelos de linguagem locais. O trabalho faz parte da pesquisa de conclusão do curso de Engenharia de Software na Universidade Federal do Ceará (UFC), Campus Quixadá.

---

## 🚀 Funcionalidades

* **🧠 Ensino Adaptativo:** O *prompt* do sistema ajusta automaticamente a complexidade da resposta (uso de analogias vs. jargões técnicos) de acordo com o nível selecionado pelo usuário.
* **📚 Base de Conhecimento RAG:** Processamento e recuperação de contexto via banco vetorial a partir de PDFs acadêmicos e *whitepapers* curados.
* **⚙️ Backend Desacoplado:** Construído com **FastAPI**, separando as regras de negócio da interface gráfica.
* **💻 Interface Interativa:** Frontend leve e dinâmico desenvolvido em **Streamlit**.
* **🔒 Privacidade Total:** Utilização do **Ollama** para rodar LLMs (como o Llama 3.1) e modelos de *embedding* (Nomic) localmente, sem depender de APIs de terceiros.

---

## 📁 Arquitetura do Projeto

A base de código foi desenhada baseada nos princípios de *Clean Architecture* e SOLID, isolando a lógica de negócio das ferramentas de infraestrutura (LangChain/ChromaDB).

```text
tutor-crypto-ai/
├── src/
│   ├── application/           # Casos de uso e DTOs da API
│   ├── infrastructure/        # LangChain, ChromaDB e ingestão de PDFs
│   └── presentation/          # Controladores (se aplicável futuramente)
├── data/                      # Base de PDFs para RAG (Módulos de estudo)
├── docs/                      # Pasta destinada para documentos do projeto
├── crypto_db/                 # Banco vetorial persistido localmente
├── app.py                     # Interface Web (Streamlit)
├── main.py                    # API REST (FastAPI)
└── CONTEXT.md                 # Entendimento completo e fluxo de execução do projeto
```

> **Nota:** Para um entendimento mais profundo sobre as decisões de arquitetura e o fluxo de dados do projeto, acesse o documento completo em **[CONTEXT.md](./CONTEXT.md)**.

---

## 🛠️ Pré-requisitos

Antes de iniciar, certifique-se de que o seu ambiente atende aos seguintes requisitos:

1. **Python 3.10+**: O projeto requer uma versão atualizada do Python.
2. **Ollama**: Ferramenta essencial para rodar os modelos de linguagem locais e garantir a privacidade dos dados.
   - [Instale o Ollama de acordo com seu SO](https://ollama.com/download)
   - Baixe os modelos necessários abrindo um terminal e executando:
     ```bash
     ollama pull llama3.1:8b
     ollama pull nomic-embed-text:latest
     ```

---

## 💻 Instalação e Execução

### 1. Configurar o Ambiente

```bash
# Clone este repositório
git clone https://github.com/josiasdev/tutor-crypto-ai.git
cd tutor-crypto-ai

# Criar e ativar o ambiente virtual (opcional, mas recomendado)
python3 -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate

# Instalar as dependências do projeto
pip install -r requirements.txt
```

### 2. Construir a Base de Conhecimento

Coloque seus documentos PDF na pasta `data/` (ex: apostilas, e-books, artigos). Em seguida, execute o script para ler os arquivos, gerar os fragmentos e as *embeddings*, e persistir tudo no banco vetorial:

```bash
python src/infrastructure/document_loaders/ingest_data.py
```
Isso criará a pasta `crypto_db/` contendo os dados vetorizados pelo ChromaDB.

### 3. Rodar a Aplicação

A aplicação é dividida em dois serviços (Backend e Frontend), que devem rodar simultaneamente.

**1️⃣ Rodar o Backend (API REST FastAPI):**
Em um terminal (com o `venv` ativado), inicie a API:
```bash
uvicorn main:app --reload
```
> *A API estará rodando em `http://localhost:8000`. Você pode acessar o Swagger UI em `http://localhost:8000/docs`.*

**2️⃣ Rodar o Frontend (Interface Streamlit):**
Abra um novo terminal, ative o `venv` novamente, e execute:
```bash
streamlit run app.py
```
> *A interface interativa será aberta no seu navegador padrão em `http://localhost:8501`.*

---

## 🤝 Como Contribuir

Contribuições para a evolução do Tutor de IA são muito bem-vindas! Siga os passos:

1. Faça um **Fork** do projeto.
2. Crie uma **Branch** para a sua funcionalidade (`git checkout -b feature/MinhaFeature`).
3. Adicione suas modificações e faça o **Commit** (`git commit -m 'Feat: Adicionando a funcionalidade X'`).
4. Faça o **Push** para a Branch original (`git push origin feature/MinhaFeature`).
5. Abra um **Pull Request**.

---

## 📄 Licença e Referência

Este projeto tem foco acadêmico e é fruto do Trabalho de Conclusão de Curso (TCC) em Engenharia de Software pela **Universidade Federal do Ceará (UFC - Campus Quixadá)**. Sinta-se à vontade para se inspirar e estender a pesquisa.