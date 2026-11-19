import streamlit as st
from typing import Callable, List
from src.application.study_suggestions import get_initial_prompts, get_continuation_prompts


def render_top_meta_bar(nivel: str, api_online: bool) -> None:
    """Exibe barra de status superior com metadados sem emojis."""
    status_class = "badge-online" if api_online else "badge-offline"
    status_text = "API Conectada" if api_online else "API Indisponível"

    html = f"""
    <div class="top-badge-container">
        <div class="top-badge-item">
            <strong>Tutor Crypto AI</strong> | Ambiente de Aprendizagem
        </div>
        <div class="top-badge-item">
            <span>Perfil: <strong>{nivel}</strong></span>
            <span>|</span>
            <span class="badge-indicator {status_class}"></span>
            <span>{status_text}</span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_welcome_and_quick_prompts(on_select_prompt: Callable[[str], None]) -> None:
    """Exibe mensagem de recepção e cards iniciais de estudo (P0)."""
    html = """
    <div class="welcome-card">
        <div class="welcome-title">O que vamos aprender hoje?</div>
        <div class="welcome-subtitle">
            Selecione uma das perguntas essenciais abaixo para iniciar seus estudos ou escreva sua dúvida no campo inferior.
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

    prompts = get_initial_prompts()
    cols = st.columns(2)

    for idx, item in enumerate(prompts):
        col = cols[idx % 2]
        with col:
            rotulo = f"[{item['tema']}] {item['pergunta']}"
            if st.button(rotulo, key=f"quick_prompt_{idx}", use_container_width=True):
                on_select_prompt(item["pergunta"])


def render_continuation_options(
    pergunta: str, resposta: str, nivel: str, on_select_prompt: Callable[[str], None]
) -> None:
    """Renderiza sugestões de aprofundamento e próximos passos (P1)."""
    sugestoes = get_continuation_prompts(pergunta, resposta, nivel)
    if not sugestoes:
        return

    st.markdown('<div class="continuation-label">Próximos passos de estudo sugeridos</div>', unsafe_allow_html=True)
    cols = st.columns(len(sugestoes))

    for idx, prompt_texto in enumerate(sugestoes):
        with cols[idx]:
            if st.button(prompt_texto, key=f"cont_prompt_{idx}", use_container_width=True):
                on_select_prompt(prompt_texto)


def render_about_page() -> None:
    """Exibe painel institucional do projeto acadêmico."""
    st.markdown("### Sobre o Projeto Acadêmico")
    st.markdown(
        """
Este sistema é parte do Trabalho de Conclusão de Curso (TCC) em **Engenharia de Software** pela **Universidade Federal do Ceará (UFC - Campus Quixadá)**.

**Objetivo:**
Investigar o papel de Agentes de Inteligência Artificial e Recuperação Aumentada de Geração (RAG) no ensino personalizado de conceitos fundamentais de Blockchain e Criptomoedas.

**Características Arquiteturais:**
- **Privacidade e Autonomia:** Modelos locais executados via Ollama (Llama 3.1 8B e Nomic Embed Text).
- **Ancoragem Documental:** Base vetorial em ChromaDB com curadoria de artigos acadêmicos, monografias e whitepapers originais.
- **Adaptação de Nível:** Ajuste dinâmico entre linguagem acessível (Iniciante) e densidade técnica arquitetural (Avançado).
- **Sem especulação financeira:** O sistema foca estritamente em aspectos técnicos, criptográficos e arquiteturais de sistemas descentralizados.
        """
    )


def render_learning_path_page(on_select_prompt: Callable[[str], None]) -> None:
    """Exibe trilha de aprendizagem estruturada."""
    st.markdown("### Trilha de Aprendizagem Recomendada")
    st.markdown("Siga a progressão conceitual sugerida ou explore diretamente os tópicos:")

    etapas = [
        {
            "modulo": "Módulo 1 - Fundamentos e Redes Descentralizadas",
            "desc": "Conceito de livro-razão distribuído, redes P2P e propriedades dos blocos.",
            "prompt": "Como funciona uma rede descentralizada P2P e qual o papel dos nós?",
        },
        {
            "modulo": "Módulo 2 - Mecanismos de Consenso",
            "desc": "Proof of Work, mineração, Proof of Stake e segurança de estado.",
            "prompt": "Qual a diferença entre Proof of Work e Proof of Stake em termos de segurança e energia?",
        },
        {
            "modulo": "Módulo 3 - Criptografia Assimétrica e Custódia",
            "desc": "Pares de chaves, derivação de endereços e segurança de carteiras digitais.",
            "prompt": "Como funcionam as chaves pública e privada para assinar transações?",
        },
        {
            "modulo": "Módulo 4 - Modelos de Transação e Contabilidade",
            "desc": "Modelo UTXO (Bitcoin) versus Modelo de Contas com balanço global (Ethereum).",
            "prompt": "Quais as vantagens de paralelismo do modelo UTXO frente ao modelo de contas?",
        },
        {
            "modulo": "Módulo 5 - Contratos Inteligentes e Máquina Virtual",
            "desc": "Execução determinística, EVM, bytecode e mecanismos de taxa (Gas).",
            "prompt": "O que são smart contracts e por que sua execução precisa ser determinística?",
        },
    ]

    for idx, etapa in enumerate(etapas):
        with st.expander(etapa["modulo"], expanded=(idx == 0)):
            st.write(etapa["desc"])
            if st.button("Estudar este módulo", key=f"path_btn_{idx}"):
                on_select_prompt(etapa["prompt"])
