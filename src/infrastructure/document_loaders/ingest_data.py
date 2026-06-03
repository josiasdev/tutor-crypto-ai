import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# --- CONFIGURAÇÃO DE CAMINHOS ABSOLUTOS ---
# Resolve dinamicamente o caminho da raiz do projeto (tutor-crypto-ai)
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_PATH = str(BASE_DIR / "data")
CHROMA_PATH = str(BASE_DIR / "crypto_db")

def criar_banco_vetorial():
    print(f"--- Iniciando a Construção da Base de Conhecimento ---")
    print(f"Buscando documentos na pasta: '{DATA_PATH}'...")
    
    # 1. Coleta: Carrega todos os PDFs do diretório
    loader = PyPDFDirectoryLoader(DATA_PATH, recursive=True)
    documentos = loader.load()

    if not documentos:
        print(f"Nenhum PDF encontrado na pasta '{DATA_PATH}'.")
        return

    print(f"{len(documentos)} páginas carregadas no total.")

    # 2. Processamento: Quebra o texto em chunks (pedaços)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(documentos)
    
    print(f"Documentos divididos em {len(chunks)} fragmentos (chunks).")
    print("Gerando embeddings e salvando no ChromaDB. Isso pode levar alguns instantes...")

    # 3. Embeddings: Conecta ao Nomic rodando no Ollama local
    embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")

    # Cria o banco vetorial e salva fisicamente no disco usando o pacote atualizado langchain_chroma
    db = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=CHROMA_PATH
    )
    
    print(f"Sucesso! Banco de dados vetorial atualizado na pasta '{CHROMA_PATH}'.")

if __name__ == "__main__":
    os.makedirs(DATA_PATH, exist_ok=True)
    criar_banco_vetorial()