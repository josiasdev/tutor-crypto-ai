def get_theme_styles(is_dark: bool = False) -> str:
    """Gera regras de CSS com suporte a Modo Claro e Modo Escuro sem quebrar o botão de toggle da sidebar."""
    if is_dark:
        bg_main = "#0B0F19"
        bg_card = "#111827"
        bg_sidebar = "#0F172A"
        border_color = "#1F2937"
        text_primary = "#F9FAFB"
        text_secondary = "#9CA3AF"
        chat_bg = "#111827"
    else:
        bg_main = "#F8FAFC"
        bg_card = "#FFFFFF"
        bg_sidebar = "#FFFFFF"
        border_color = "#E2E8F0"
        text_primary = "#0F172A"
        text_secondary = "#64748B"
        chat_bg = "#FFFFFF"

    return f"""
    <style>
    /* Ajuste de espaçamento central */
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 860px !important;
    }}

    /* Esconde o menu de opções nativo e o footer, mas MANTÉM visível o botão de recolher/expandir sidebar */
    #MainMenu, footer {{
        visibility: hidden;
    }}

    /* Garante visibilidade e posicionamento adequado do cabeçalho da sidebar para abrir/fechar */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"] {{
        visibility: visible !important;
        display: flex !important;
    }}

    /* Cores de fundo e texto dinâmicas */
    .stApp {{
        background-color: {bg_main} !important;
        color: {text_primary} !important;
    }}

    section[data-testid="stSidebar"] {{
        background-color: {bg_sidebar} !important;
        border-right: 1px solid {border_color} !important;
    }}

    /* Tipografia institucional */
    html, body, [class*="css"] {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        color: {text_primary};
    }}

    /* Divisor linear customizado */
    .academic-divider {{
        height: 1px;
        background: {border_color};
        margin: 1.25rem 0;
        border: none;
    }}

    /* Painel superior com metadados */
    .top-badge-container {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.65rem 1rem;
        background: {bg_card};
        border: 1px solid {border_color};
        border-radius: 6px;
        margin-bottom: 1.5rem;
        font-size: 0.85rem;
        color: {text_secondary};
    }}

    .top-badge-item {{
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        color: {text_secondary};
    }}

    .top-badge-item strong {{
        color: {text_primary};
    }}

    /* Painel de boas-vindas */
    .welcome-card {{
        background: {bg_card};
        border: 1px solid {border_color};
        border-radius: 8px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.5rem;
    }}

    .welcome-title {{
        font-size: 1.2rem;
        font-weight: 600;
        color: {text_primary};
        margin-bottom: 0.3rem;
    }}

    .welcome-subtitle {{
        font-size: 0.92rem;
        color: {text_secondary};
        line-height: 1.4;
    }}

    /* Legenda de continuidade */
    .continuation-label {{
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: {text_secondary};
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }}

    /* Balões de chat */
    div[data-testid="stChatMessage"] {{
        background: {chat_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        margin-bottom: 0.8rem !important;
        color: {text_primary} !important;
    }}

    div[data-testid="stChatMessage"] p,
    div[data-testid="stChatMessage"] span,
    div[data-testid="stChatMessage"] strong {{
        color: {text_primary} !important;
    }}
    </style>
    """
