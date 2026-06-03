import streamlit as st
import requests

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Tutor de IA - Web3", page_icon="🪙", layout="centered")

# URL da nossa API FastAPI (ajuste se estiver rodando em outra porta)
API_URL = "http://localhost:8000/api/v1/chat"

# --- INTERFACE DO USUÁRIO (UI) ---
st.title("🪙 Tutor IA: Cripto & Blockchain")
st.markdown("Faça perguntas sobre os documentos da base de conhecimento e veja a IA adaptar a didática ao seu nível.")

# Menu Lateral (Sidebar)
with st.sidebar:
    st.header("⚙️ Configurações de Tutoria")
    nivel_selecionado = st.radio(
        "Selecione o nível de dificuldade:",
        ("Iniciante", "Avançado"),
        help="Altera a forma como o Agente de IA explica os conceitos."
    )
    
    st.divider()
    if st.button("Limpar Histórico de Chat"):
        st.session_state.messages = []
        st.rerun()

# --- GERENCIAMENTO DE ESTADO DO CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens antigas na tela
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LOOP PRINCIPAL DO CHAT ---
if prompt_usuario := st.chat_input("Ex: O que é o Proof of Work?"):
    
    # 1. Adiciona e exibe a mensagem do usuário
    with st.chat_message("user"):
        st.markdown(prompt_usuario)
    st.session_state.messages.append({"role": "user", "content": prompt_usuario})

    # 2. Chama a API FastAPI para processar a resposta
    with st.chat_message("assistant"):
        with st.spinner(f"Consultando API (Nível: {nivel_selecionado})..."):
            try:
                # Monta o corpo da requisição (Payload)
                payload = {
                    "pergunta": prompt_usuario,
                    "nivel": nivel_selecionado
                }
                
                # Faz a requisição POST para o FastAPI
                response = requests.post(API_URL, json=payload)
                
                # Verifica se a requisição deu certo (Status 200)
                if response.status_code == 200:
                    dados = response.json()
                    texto_resposta = dados["resposta"]
                    st.markdown(texto_resposta)
                    
                    # 3. Salva a resposta no histórico
                    st.session_state.messages.append({"role": "assistant", "content": texto_resposta})
                else:
                    st.error(f"Erro na API: {response.status_code} - {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("🚨 Não foi possível conectar à API. Verifique se o servidor FastAPI (uvicorn) está rodando em localhost:8000.")