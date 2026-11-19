def get_clean_styles() -> str:
    """Retorna estilos CSS para eliminar estética padrão e aplicar design acadêmico/sóbrio."""
    return """
    <style>
    /* Remove padding superior desnecessário e cabeçalho padrão */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 860px !important;
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    /* Tipografia institucional limpa */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        color: #0F172A;
    }

    /* Divisores customizados sutis sem traços múltiplos */
    .academic-divider {
        height: 1px;
        background: #E2E8F0;
        margin: 1.5rem 0;
        border: none;
    }

    /* Painel superior com metadados */
    .top-badge-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.6rem 0.9rem;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        margin-bottom: 1.5rem;
        font-size: 0.85rem;
        color: #64748B;
    }

    .top-badge-item {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
    }

    .badge-indicator {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
    }

    .badge-online {
        background-color: #14B8A6;
    }

    .badge-offline {
        background-color: #DC2626;
    }

    /* Painel de boas-vindas acolhedor e sóbrio */
    .welcome-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.5rem;
    }

    .welcome-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #0F172A;
        margin-bottom: 0.3rem;
    }

    .welcome-subtitle {
        font-size: 0.92rem;
        color: #64748B;
        line-height: 1.4;
    }

    /* Estilização de chips de continuidade */
    .continuation-label {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }

    /* Ajuste fino dos balões de chat nativos */
    div[data-testid="stChatMessage"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.8rem;
    }
    </style>
    """
