import streamlit as st
from typing import Callable, List
from src.application.study_suggestions import get_initial_prompts, get_continuation_prompts


def render_welcome_and_quick_prompts(on_select_prompt: Callable[[str], None]) -> None:
    """Exibe os cards clicáveis de perguntas iniciais integrados ao layout padrão."""
    st.write("Escolha uma pergunta para começar ou digite sua dúvida abaixo:")
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
    """Renderiza sugestões de aprofundamento e próximos passos após uma resposta."""
    sugestoes = get_continuation_prompts(pergunta, resposta, nivel)
    if not sugestoes:
        return

    st.write("**Próximos passos de estudo sugeridos:**")
    cols = st.columns(len(sugestoes))

    for idx, prompt_texto in enumerate(sugestoes):
        with cols[idx]:
            if st.button(prompt_texto, key=f"cont_prompt_{idx}", use_container_width=True):
                on_select_prompt(prompt_texto)
