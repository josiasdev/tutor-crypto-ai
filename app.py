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

# URL da nossa API FastAPI
API_URL = "http://localhost:8000/api/v1/chat"

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

    # 2. Chama a API FastAPI para processar a resposta
    with st.chat_message("assistant"):
        with st.spinner(f"Consultando API (Nível: {nivel_selecionado})..."):
            try:
                payload = {
                    "pergunta": prompt_to_process,
                    "nivel": nivel_selecionado,
                }
                response = requests.post(API_URL, json=payload, timeout=60)

                if response.status_code == 200:
                    dados = response.json()
                    texto_resposta = dados["resposta"]
                    st.markdown(f"**Tutor**\n\n{texto_resposta}")
                    st.session_state.messages.append(
                        {"role": "assistant", "content": texto_resposta}
                    )
                    st.rerun()
                else:
                    st.error(f"Erro na API: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException:
                st.error(
                    "Não foi possível conectar à API. Verifique se o servidor FastAPI (uvicorn) está rodando em localhost:8000."
                )
