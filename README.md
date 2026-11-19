# Agente de IA: Tutor Personalizado no Ensino de Criptomoedas e Blockchain

![Status](https://img.shields.io/badge/Status-TCC%202%20%7C%20Fase%202-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111%2B-009688)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B)
![LangChain](https://img.shields.io/badge/LangChain-0.2%2B-green)

Este projeto apresenta o desenvolvimento de um Agente de Inteligência Artificial concebido para atuar como Sistema Tutor Inteligente (ITS) personalizado no ensino de Criptomoedas e tecnologia Blockchain.

O sistema adapta dinamicamente a profundidade pedagógica das explicações (entre os perfis Iniciante e Avançado) por meio da arquitetura de Recuperação Aumentada de Geração (RAG) executada com modelos de linguagem locais. A pesquisa integra o Trabalho de Conclusão de Curso (TCC 1 e TCC 2) em Engenharia de Software na Universidade Federal do Ceará (UFC), Campus Quixadá.

---

## Escopo e Evolução do Projeto (TCC 1 e TCC 2)

### Fase 1: TCC 1 (Concluída)
- [x] Levantamento bibliográfico e definição da arquitetura desacoplada (Streamlit + FastAPI)
- [x] Curadoria da base documental em Português do Brasil (pt-BR), publicada no Google Drive como `Corpus_RAG_Tutor_Blockchain_Criptomoedas_PTBR`, e pipeline de ingestão vetorial (ChromaDB + Nomic)
- [x] Orquestração do agente tutor via LangChain Expression Language (LCEL) com prompt adaptativo
- [x] Bateria de testes técnicos exploratórios (CT-01 a CT-06) cobrindo Blockchain, Criptomoedas e bloqueio de alucinações

### Fase 2: TCC 2 (Em Andamento)
- [x] Melhorias iterativas no frontend (Streamlit): persistência do histórico de sessão e refinamento da interface de estudo
- [x] Estruturação dos questionários de avaliação em Escala Likert de 5 pontos (usabilidade, clareza didática e utilidade percebida)
- [x] Realização dos testes empíricos de usabilidade com discentes voluntários da UFC Campus Quixadá
- [x] Tabulação e análise quantitativa e qualitativa dos dados coletados
- [ ] Redação final dos resultados e conclusões consolidadas
- [ ] Ajustes finais de formatação ABNT e defesa do TCC 2

---

## Funcionalidades Principais

- **Ensino Adaptativo (Scaffolding Cognitivo):** O prompt de sistema ajusta o vocabulário e a densidade conceitual conforme o nível selecionado pelo estudante (analogias cotidianas no perfil Iniciante versus formalismo criptográfico e arquitetural no perfil Avançado).
- **Base de Conhecimento Curada (RAG):** Recuperação semântica (`Top-k = 3`) restrita a materiais técnicos e acadêmicos em português do Brasil, mitigando alucinações factuais. O corpus completo é auditável no Google Drive (veja a seção [Base Documental](#base-documental-corpus-rag)).
- **Backend Desacoplado:** API REST construída com FastAPI, separando regras de negócio, controle de sessão via JWT e serviços de inferência.
- **Interface Web Iterativa:** Frontend desenvolvido em Streamlit com seleção dinâmica de perfil, histórico de conversas por sessão e navegação orientada aos eixos de Criptomoedas e Blockchain.
- **Privacidade e Execução Local:** Inferência local via Ollama utilizando Llama 3 (8B) e Nomic Embed Text, sem envio de dados acadêmicos para APIs proprietárias externas.

---

## Base Documental (Corpus RAG)

Os documentos indexados no ChromaDB estão disponíveis em uma pasta pública do Google Drive (permissão: qualquer pessoa com o link pode visualizar), para que a banca examinadora audite exatamente as fontes utilizadas:

**Pasta no Google Drive:** `Corpus_RAG_Tutor_Blockchain_Criptomoedas_PTBR`
**Link:** https://drive.google.com/drive/folders/1SmvehVVuuy3lIpNitD3cV0lAm22S09CX

```text
Corpus_RAG_Tutor_Blockchain_Criptomoedas_PTBR/
├── 01_Tecnologia_Blockchain/        # Blocos, hash, redes P2P, consenso (PoW/PoS) e contratos inteligentes
├── 02_Criptomoedas/                 # Ativos digitais, criptografia assimétrica, carteiras, custódia e modelos UTXO/Contas
└── README_Criterios_Curadoria       # Critérios de inclusão, catálogo dos PDFs e parâmetros de ingestão
```

Critérios de curadoria resumidos: arquivos exclusivamente em PDF, em português do Brasil, com camada de texto nativa (sem OCR), provenientes de whitepapers, publicações de instituições reguladoras, material acadêmico e monografias, sem conteúdo opinativo ou promocional. O catálogo completo, com a fonte de cada arquivo, está no documento `README_Criterios_Curadoria` dentro da própria pasta.

---

## Arquitetura e Estrutura de Diretórios

A base de código segue os princípios de Clean Architecture e SOLID, isolando os casos de uso da aplicação dos detalhes de infraestrutura (LangChain, ChromaDB e Ollama).

```text
tutor-crypto-ai/
├── src/
│   ├── application/                 # Casos de uso (ChatTutorUseCase) e DTOs da API
│   ├── infrastructure/              # Orquestração LangChain (LCEL), ChromaDB e ingestão
│   │   ├── document_loaders/        # Pipeline de extração, chunking e embeddings
│   │   └── rag_service.py           # Serviço do agente tutor e prompt adaptativo
│   └── presentation/                # Rotas FastAPI e middleware de autenticação JWT
├── data/                            # Cópia local do corpus (Drive: Corpus_RAG_Tutor_Blockchain_Criptomoedas_PTBR)
│   ├── 01_Tecnologia_Blockchain/    # Fundamentos de blocos, consenso (PoW/PoS) e contratos
│   └── 02_Criptomoedas/             # Criptografia assimétrica, carteiras e modelos UTXO/Contas
├── docs/                            # Documentação técnica e instrumentos da Fase 2
│   └── avaliacao/                   # Questionário Escala Likert e protocolo empírico
├── tests/                           # Testes de integração e casos de teste funcionais (CT-01..06)
├── crypto_db/                       # Banco vetorial ChromaDB persistido localmente
├── app.py                           # Interface Web interativa (Streamlit)
├── main.py                          # Ponto de entrada da API REST (FastAPI)
├── CONTEXT.md                       # Especificação arquitetural e fluxo detalhado do sistema
└── requirements.txt                 # Dependências do projeto Python
```

---

## Pré-requisitos

Antes de iniciar, certifique-se de que o seu ambiente atende aos seguintes requisitos:

1. Python 3.10 ou superior instalado no ambiente.
2. Ollama instalado e em execução local para servir o LLM e o modelo de embeddings:
   - [Instale o Ollama de acordo com seu SO](https://ollama.com/download)
   - Baixe os modelos necessários via terminal:
     ```bash
     ollama pull llama3.1:8b
     ollama pull nomic-embed-text:latest
     ```

---

## Instalação e Execução

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

Baixe a pasta `Corpus_RAG_Tutor_Blockchain_Criptomoedas_PTBR` do Google Drive (link na seção [Base Documental](#base-documental-corpus-rag)) e coloque os PDFs dentro de `data/`, mantendo as subpastas `01_Tecnologia_Blockchain/` e `02_Criptomoedas/`. Em seguida, execute o script para ler os arquivos, gerar os fragmentos e as *embeddings*, e persistir tudo no banco vetorial:

```bash
python src/infrastructure/document_loaders/ingest_data.py
```
O carregamento é recursivo (`PyPDFDirectoryLoader`), então as subpastas são lidas automaticamente. Isso criará a pasta `crypto_db/` contendo os dados vetorizados pelo ChromaDB.

### 3. Rodar a Aplicação

A aplicação é dividida em dois serviços (Backend e Frontend), que devem rodar simultaneamente.

**1. Rodar o Backend (API REST FastAPI):**
Em um terminal (com o `venv` ativado), inicie a API:
```bash
uvicorn main:app --reload
```
> *A API estará rodando em `http://localhost:8000`. Você pode acessar o Swagger UI em `http://localhost:8000/docs`.*

**2. Rodar o Frontend (Interface Streamlit):**
Abra um novo terminal, ative o `venv` novamente, e execute:
```bash
streamlit run app.py
```
> *A interface interativa será aberta no seu navegador padrão em `http://localhost:8501`.*

---

## Como Contribuir

Contribuições para a evolução do Tutor de IA são muito bem-vindas! Siga os passos:

1. Faça um **Fork** do projeto.
2. Crie uma **Branch** para a sua funcionalidade (`git checkout -b feature/MinhaFeature`).
3. Adicione suas modificações e faça o **Commit** (`git commit -m 'Feat: Adicionando a funcionalidade X'`).
4. Faça o **Push** para a Branch original (`git push origin feature/MinhaFeature`).
5. Abra um **Pull Request**.

---

## Licença e Referência

Este projeto tem foco acadêmico e é fruto do Trabalho de Conclusão de Curso (TCC) em Engenharia de Software pela **Universidade Federal do Ceará (UFC - Campus Quixadá)**. Sinta-se à vontade para se inspirar e estender a pesquisa.