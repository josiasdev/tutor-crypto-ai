import os
from pathlib import Path
import streamlit as st
import requests
from src.presentation.components import (
    render_welcome_and_quick_prompts,
    render_continuation_options,
)

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Tutor IA - Cripto & Blockchain",
    layout="centered",
)

# URL da nossa API FastAPI ou fallback para chamada direta do UseCase
API_URL = "http://127.0.0.1:8000/api/v1/chat"

# --- INTERFACE DO USUÁRIO (UI) ---
st.title("Tutor IA: Cripto & Blockchain")
st.markdown("Faça perguntas sobre os documentos da base de conhecimento e veja a IA adaptar a didática ao seu nível.")

# Menu Lateral (Sidebar)
with st.sidebar:
    st.header("Configurações de Tutoria")
    nivel_selecionado = st.radio(
        "Selecione o nível de dificuldade:",
        ("Iniciante", "Avançado"),
        help="Altera a forma como o Agente de IA explica os conceitos.",
    )

    if st.button("Limpar Histórico de Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()

# --- GERENCIAMENTO DE ESTADO DO CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


def submit_prompt(prompt_text: str):
    st.session_state.pending_prompt = prompt_text
    st.rerun()


@st.cache_resource
def get_local_use_case():
    """Fallback inteligente para executar inferência local sem depender de porta HTTP externa aberta."""
    from src.infrastructure.rag_service import TutorRAGService
    from src.application.use_cases import ChatTutorUseCase
    return ChatTutorUseCase(rag_service=TutorRAGService())


def processar_pergunta(pergunta: str, nivel: str) -> str:
    """Tenta consultar via API FastAPI; se a porta HTTP estiver indisponível, usa o serviço local direto."""
    try:
        payload = {"pergunta": pergunta, "nivel": nivel}
        response = requests.post(API_URL, json=payload, timeout=5)
        if response.status_code == 200:
            return response.json()["resposta"]
    except Exception:
        pass

    # Execução direta do pipeline RAG caso a porta 8000 esteja ocupada ou fechada
    use_case = get_local_use_case()
    from src.application.dtos import ChatRequest
    resultado = use_case.executar(ChatRequest(pergunta=pergunta, nivel=nivel))
    return resultado.resposta


# Se o chat estiver vazio, exibe as perguntas sugeridas de início rápido
if not st.session_state.messages:
    render_welcome_and_quick_prompts(on_select_prompt=submit_prompt)

# Exibe as mensagens antigas na tela
for message in st.session_state.messages:
    avatar_label = "Você" if message["role"] == "user" else "Tutor"
    with st.chat_message(message["role"]):
        st.markdown(f"**{avatar_label}**\n\n{message['content']}")

# Renderiza opções de continuidade após a última resposta do tutor
if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    last_question = ""
    for m in reversed(st.session_state.messages):
        if m["role"] == "user":
            last_question = m["content"]
            break
    last_answer = st.session_state.messages[-1]["content"]
    render_continuation_options(
        pergunta=last_question,
        resposta=last_answer,
        nivel=nivel_selecionado,
        on_select_prompt=submit_prompt,
    )

# --- CAPTURA DE PROMPT ---
user_input = st.chat_input("Ex: O que é o Proof of Work?")
prompt_to_process = None

if user_input:
    prompt_to_process = user_input
elif st.session_state.pending_prompt:
    prompt_to_process = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

if prompt_to_process:
    # 1. Adiciona e exibe a mensagem do usuário
    with st.chat_message("user"):
        st.markdown(f"**Você**\n\n{prompt_to_process}")
    st.session_state.messages.append({"role": "user", "content": prompt_to_process})

    # 2. Gera a resposta do Tutor (com spinner adaptado)
    with st.chat_message("assistant"):
        with st.spinner(f"Consultando materiais do corpus (Nível: {nivel_selecionado})..."):
            try:
                texto_resposta = processar_pergunta(prompt_to_process, nivel_selecionado)
                st.markdown(f"**Tutor**\n\n{texto_resposta}")
                st.session_state.messages.append(
                    {"role": "assistant", "content": texto_resposta}
                )
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao processar consulta: {str(e)}")
