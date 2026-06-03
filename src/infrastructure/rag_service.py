from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

def formatar_docs(docs):
    """Função auxiliar para juntar o texto dos documentos recuperados."""
    return "\n\n".join(doc.page_content for doc in docs)

class TutorRAGService:
    def __init__(self, chroma_path: str = "crypto_db"):
        self.chroma_path = chroma_path
        self._configurar_chain()

    def _configurar_chain(self):
        # 1. Configura Embeddings e Banco Vetorial
        embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")
        db = Chroma(persist_directory=self.chroma_path, embedding_function=embeddings)
        retriever = db.as_retriever(search_kwargs={"k": 3})

        # 2. Configura o LLM local
        llm = ChatOllama(model="llama3.1:8b", temperature=0.3)

        # 3. Configura o Prompt Adaptativo
        system_prompt = (
            "Você é um tutor acadêmico especializado em Criptomoedas e Blockchain. "
            "Seu objetivo é ensinar o usuário com base estritamente no contexto fornecido. "
            "O nível atual de conhecimento do usuário é: {nivel_usuario}. "
            "Se o nível for 'Iniciante', use analogias simples e evite jargões sem explicá-los. "
            "Se o nível for 'Avançado', use linguagem técnica e detalhes de arquitetura. "
            "Se não souber a resposta com base no contexto, diga que não encontrou no material. "
            "\n\nContexto extraído dos PDFs:\n{context}"
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])

        # 4. Configura as funções de extração de variáveis
        extrair_pergunta = RunnableLambda(lambda x: x["input"])

        # 5. Constrói a Pipeline RAG com LCEL
        self.rag_chain = (
            {
                "context": extrair_pergunta | retriever | formatar_docs,
                "input": RunnablePassthrough() | extrair_pergunta,
                "nivel_usuario": RunnableLambda(lambda x: x["nivel_usuario"]),
            }
            | prompt
            | llm
            | StrOutputParser() # Garante que a saída final será apenas texto
        )

    def gerar_resposta(self, pergunta: str, nivel: str) -> str:
        """
        Injeta as variáveis na pipeline RAG e retorna a resposta do tutor.
        """
        # Como usamos o StrOutputParser, o 'invoke' retorna direto a string final
        resultado_texto = self.rag_chain.invoke({
            "input": pergunta,
            "nivel_usuario": nivel
        })
        
        return resultado_texto