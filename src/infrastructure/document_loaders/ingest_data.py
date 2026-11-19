import os
from pathlib import Path
from tqdm import tqdm
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# --- CONFIGURAÇÃO DE CAMINHOS ABSOLUTOS ---
# Resolve dinamicamente o caminho da raiz do projeto (tutor-crypto-ai)
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_PATH = str(BASE_DIR / "data")
CHROMA_PATH = str(BASE_DIR / "crypto_db")
BATCH_SIZE = 50  # Tamanho do lote para embeddings e progresso


def criar_banco_vetorial():
    print("--- Iniciando a Construção da Base de Conhecimento ---")
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

    # Sanitiza os textos para evitar UnicodeEncodeError com caracteres estranhos de PDFs
    for chunk in chunks:
        chunk.page_content = chunk.page_content.encode("utf-8", "replace").decode("utf-8")

    print(f"Documentos divididos em {len(chunks)} fragmentos (chunks).")
    print("Gerando embeddings e salvando no ChromaDB:")

    # 3. Embeddings: Conecta ao Nomic rodando no Ollama local
    embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")

    # Inicializa ou abre o banco vetorial ChromaDB persistido
    db = Chroma(
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH,
    )

    # Ingestão em lotes com barra de progresso (tqdm)
    total_chunks = len(chunks)
    with tqdm(total=total_chunks, desc="Progresso da Ingestão", unit="chunk") as pbar:
        for i in range(0, total_chunks, BATCH_SIZE):
            lote = chunks[i : i + BATCH_SIZE]
            db.add_documents(documents=lote)
            pbar.update(len(lote))

    print(f"Sucesso! Banco de dados vetorial atualizado na pasta '{CHROMA_PATH}'.")


if __name__ == "__main__":
    os.makedirs(DATA_PATH, exist_ok=True)
    criar_banco_vetorial()
