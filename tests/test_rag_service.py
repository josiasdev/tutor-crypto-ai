from unittest.mock import MagicMock, patch
from langchain_core.documents import Document

from src.infrastructure.rag_service import formatar_docs, TutorRAGService


class TestRAGServiceUnit:
    """Testes unitários para o serviço RAG e pipeline LCEL."""

    def test_formatar_docs(self):
        doc1 = Document(page_content="Primeiro fragmento sobre PoW.")
        doc2 = Document(page_content="Segundo fragmento sobre PoS.")
        resultado = formatar_docs([doc1, doc2])

        assert "Primeiro fragmento sobre PoW." in resultado
        assert "Segundo fragmento sobre PoS." in resultado
        assert "\n\n" in resultado

    def test_formatar_docs_empty(self):
        resultado = formatar_docs([])
        assert resultado == ""

    @patch("src.infrastructure.rag_service.OllamaEmbeddings")
    @patch("src.infrastructure.rag_service.Chroma")
    @patch("src.infrastructure.rag_service.ChatOllama")
    def test_tutor_rag_service_initialization(
        self, mock_chat_ollama, mock_chroma, mock_embeddings
    ):
        mock_retriever = MagicMock()
        mock_chroma.return_value.as_retriever.return_value = mock_retriever

        service = TutorRAGService(chroma_path="fake_crypto_db")

        assert service.chroma_path == "fake_crypto_db"
        assert hasattr(service, "rag_chain")
        mock_embeddings.assert_called_once_with(model="nomic-embed-text:latest")
        mock_chroma.assert_called_once_with(
            persist_directory="fake_crypto_db",
            embedding_function=mock_embeddings.return_value
        )
        mock_chroma.return_value.as_retriever.assert_called_once_with(
            search_kwargs={"k": 3}
        )

    @patch("src.infrastructure.rag_service.OllamaEmbeddings")
    @patch("src.infrastructure.rag_service.Chroma")
    @patch("src.infrastructure.rag_service.ChatOllama")
    def test_tutor_rag_service_gerar_resposta(
        self, mock_chat_ollama, mock_chroma, mock_embeddings
    ):
        service = TutorRAGService(chroma_path="fake_crypto_db")
        service.rag_chain = MagicMock()
        service.rag_chain.invoke.return_value = "Explicação adaptada do tutor."

        resposta = service.gerar_resposta(
            pergunta="O que é consenso?",
            nivel="Iniciante"
        )

        assert resposta == "Explicação adaptada do tutor."
        service.rag_chain.invoke.assert_called_once_with({
            "input": "O que é consenso?",
            "nivel_usuario": "Iniciante"
        })
