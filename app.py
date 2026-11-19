import streamlit as st
import requests

from src.presentation.styles import get_clean_styles
from src.presentation.components import (
    render_top_meta_bar,
    render_welcome_and_quick_prompts,
    render_continuation_options,
    render_about_page,
    render_learning_path_page,
)

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Tutor Crypto AI - Ambiente de Aprendizagem",
    layout="centered",
    initial_sidebar_state="expanded",
)

API_BASE_URL = "http://localhost:8000"
API_CHAT_URL = f"{API_BASE_URL}/api/v1/chat"
API_HEALTH_URL = f"{API_BASE_URL}/health"

# Injeta CSS de tema limpo
st.markdown(get_clean_styles(), unsafe_allow_html=True)


def check_api_status() -> bool:
    try:
        resp = requests.get(API_HEALTH_URL, timeout=1.5)
        return resp.status_code == 200
    except requests.exceptions.RequestException:
        return False


api_online = check_api_status()

# --- BARRA LATERAL (NAVEGAÇÃO E CONFIGURAÇÃO) ---
with st.sidebar:
    st.markdown("### Navegação")
    menu_selecionado = st.radio(
        "Selecione a visualização:",
        ("Tutor", "Trilha de Aprendizagem", "Sobre o Projeto"),
        label_visibility="collapsed",
    )

    st.markdown('<div class="academic-divider"></div>', unsafe_allow_html=True)
    st.markdown("### Configurações Didáticas")
    nivel_selecionado = st.radio(
        "Perfil do Estudante:",
        ("Iniciante", "Avançado"),
        help="Iniciante: metáforas e linguagem acessível. Avançado: terminologia formal e detalhes de arquitetura.",
    )

    st.markdown('<div class="academic-divider"></div>', unsafe_allow_html=True)
    if st.button("Reiniciar Sessão de Estudo", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()

# --- ESTADO DA SESSÃO ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


def submit_prompt(prompt_text: str):
    st.session_state.pending_prompt = prompt_text
    st.rerun()


# --- CORPO PRINCIPAL ---
render_top_meta_bar(nivel=nivel_selecionado, api_online=api_online)

if menu_selecionado == "Sobre o Projeto":
    render_about_page()

elif menu_selecionado == "Trilha de Aprendizagem":
    render_learning_path_page(on_select_prompt=submit_prompt)

else:
    # Visualização: Tutor
    if not st.session_state.messages:
        render_welcome_and_quick_prompts(on_select_prompt=submit_prompt)

    # Exibe o histórico de mensagens
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

    # Captura prompt digitado ou acionado via botões de sugestão
    user_input = st.chat_input("Digite sua dúvida sobre Blockchain ou Criptomoedas...")
    prompt_to_process = None

    if user_input:
        prompt_to_process = user_input
    elif st.session_state.pending_prompt:
        prompt_to_process = st.session_state.pending_prompt
        st.session_state.pending_prompt = None

    if prompt_to_process:
        # Exibe pergunta do usuário
        with st.chat_message("user"):
            st.markdown(f"**Você**\n\n{prompt_to_process}")
        st.session_state.messages.append({"role": "user", "content": prompt_to_process})

        # Consulta API
        with st.chat_message("assistant"):
            with st.spinner("Consultando materiais do corpus documental..."):
                try:
                    payload = {
                        "pergunta": prompt_to_process,
                        "nivel": nivel_selecionado,
                    }
                    response = requests.post(API_CHAT_URL, json=payload, timeout=60)

                    if response.status_code == 200:
                        texto_resposta = response.json()["resposta"]
                        st.markdown(f"**Tutor**\n\n{texto_resposta}")
                        st.session_state.messages.append(
                            {"role": "assistant", "content": texto_resposta}
                        )
                        st.rerun()
                    else:
                        st.error(f"Erro na API (Status {response.status_code}): {response.text}")
                except requests.exceptions.RequestException:
                    st.error(
                        "Serviço indisponível no momento. Certifique-se de que a API FastAPI está em execução na porta 8000."
                    )
